"""
Certificate generation using the SVG template.
Converts SVG → PNG → PDF using cairosvg + pypdf.
"""
from io import BytesIO

import cairosvg
from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, NameObject, DictionaryObject, NumberObject

from django.conf import settings


def generate_certificate_pdf(student, percentage, semester, issued_date, verify_url):
    """
    Generate a certificate PDF from the SVG template with substituted student data.
    Returns the PDF bytes.
    """
    # Load the SVG template
    svg_path = str(settings.BASE_DIR / "templates" / "certificates" / "hi.svg")
    with open(svg_path, "r") as f:
        svg_content = f.read()

    # Get dynamic data
    from core.models import Course, Module, Submission, User as UserModel
    faculty_coordinator = _get_faculty_coordinator(student)

    completed_modules = Module.objects.filter(
        questions__submissions__student=student,
        questions__submissions__status=Submission.Status.ACCEPTED,
        is_active=True
    ).distinct()
    course_names = Course.objects.filter(
        modules__in=completed_modules
    ).values_list('name', flat=True).distinct()
    course_name = ", ".join(course_names) if course_names.exists() else "CCE e-Lab Programming Course"

    hod = UserModel.objects.filter(role=UserModel.Role.HOD).first()
    hod_name = hod.display_name if hod else "Head of Department"
    principal = UserModel.objects.filter(role=UserModel.Role.ADMIN).first()
    principal_name = principal.display_name if principal else "Principal / Director"

    # Substitute placeholders
    svg_content = svg_content.replace("{NAME}", student.display_name.upper())
    svg_content = svg_content.replace("{USN}", (student.usn or student.username).upper())
    svg_content = svg_content.replace("{course name}", course_name)
    svg_content = svg_content.replace("{dd/mm/yyyy}", issued_date)
    svg_content = svg_content.replace("{FACULTY_NAME}",
        faculty_coordinator.display_name.upper() if faculty_coordinator else "FACULTY COORDINATOR")
    svg_content = svg_content.replace("{fac_grade}", "Course Faculty")

    # Convert SVG to PNG (A4 landscape at ~150 DPI)
    png_data = cairosvg.svg2png(
        bytestring=svg_content.encode(),
        output_width=1684,
        output_height=1191,
    )

    # Create PDF
    writer = PdfWriter()
    page = writer.add_blank_page(width=1684, height=1191)

    # Prepare image data
    from PIL import Image as PILImage
    buf = BytesIO()
    img = PILImage.open(BytesIO(png_data))
    img_buf = BytesIO()
    img.save(img_buf, 'PNG')
    img_buf.seek(0)
    image_data = img_buf.read()

    # Create image stream in PDF
    img_stream = DecodedStreamObject()
    img_stream.set_data(image_data)
    img_stream[NameObject("/Filter")] = NameObject("/DCTDecode")
    img_stream[NameObject("/ColorSpace")] = NameObject("/DeviceRGB")
    img_stream[NameObject("/BitsPerComponent")] = NumberObject(8)
    img_stream[NameObject("/Width")] = NumberObject(img.width)
    img_stream[NameObject("/Height")] = NumberObject(img.height)
    img_ref = writer._add_object(img_stream)

    # Update page resources
    if "/Resources" not in page:
        page[NameObject("/Resources")] = DictionaryObject()
    resources = page["/Resources"]
    if "/XObject" not in resources:
        resources[NameObject("/XObject")] = DictionaryObject()
    xobjects = resources["/XObject"]
    xobjects[NameObject("/Im1")] = img_ref

    # Add image to content stream
    content = page.get_contents()
    if content is None:
        content_stream = DecodedStreamObject()
        content_stream.set_data(b"")
        content = writer._add_object(content_stream)
        page[NameObject("/Contents")] = content

    draw_cmd = f"q {img.width} 0 0 {img.height} 0 0 cm /Im1 Do Q"
    current_data = content.get_data() if hasattr(content, "get_data") else b""
    new_data = draw_cmd.encode() + b"\n" + current_data
    content.set_data(new_data)

    # Write PDF
    out = BytesIO()
    writer.write(out)
    return out.getvalue()


def _get_faculty_coordinator(student):
    """Get the faculty coordinator for a student based on completed modules."""
    from core.models import Course, Module, Submission, User as UserModel
    from django.db.models import Count, Q

    completed_modules = Module.objects.filter(
        questions__submissions__student=student,
        questions__submissions__status=Submission.Status.ACCEPTED,
        is_active=True
    ).distinct()

    if not completed_modules.exists():
        return None

    courses = Course.objects.filter(modules__in=completed_modules).annotate(
        completion_count=Count(
            "modules__questions__submissions",
            filter=Q(
                modules__questions__submissions__student=student,
                modules__questions__submissions__status=Submission.Status.ACCEPTED,
            ),
            distinct=True,
        )
    ).order_by("-completion_count")

    top_course = courses.first()
    if top_course:
        return top_course.managing_faculty.first()
    return None
