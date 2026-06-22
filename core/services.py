from io import BytesIO
from pathlib import Path

import qrcode
from django.conf import settings
from django.core.files.base import ContentFile
from django.db.models import Count, Q
from django.template.loader import render_to_string
from django.utils import timezone

from .models import Certificate, Module, Progress, Question, Submission
from .sandbox import run_c_code


JUDGE0_STATUS_MAP = {
    3: Submission.Status.ACCEPTED,
    4: Submission.Status.WRONG_ANSWER,
    5: Submission.Status.TLE,
    6: Submission.Status.COMPILE_ERROR,
    11: Submission.Status.RUNTIME_ERROR,
}


def normalize_output(value):
    return (value or "").replace("\r\n", "\n").strip()


def evaluate_submission(submission_id):
    submission = Submission.objects.select_related("question", "student").get(pk=submission_id)
    question = submission.question
    tests = list(question.test_cases.filter(is_sample=False))
    if not tests:
        tests = list(question.test_cases.all())

    submission.status = Submission.Status.RUNNING
    submission.save(update_fields=["status"])

    passed = 0
    outputs = []
    worst_status = Submission.Status.ACCEPTED
    max_time = 0.0
    max_memory = 0

    try:
        for test in tests:
            result = run_c_code(
                source_code=submission.code,
                stdin=test.stdin,
                expected_output=test.expected_output,
                time_limit=question.time_limit,
                memory_limit_kb=question.memory_limit_kb,
            )
            status_id = result.get("status_id")
            status = JUDGE0_STATUS_MAP.get(status_id, Submission.Status.INTERNAL_ERROR)
            outputs.append(normalize_output(result.get("stdout")))

            max_time = max(max_time, float(result.get("time") or 0))
            max_memory = max(max_memory, int(result.get("memory") or 0))

            if status == Submission.Status.ACCEPTED:
                passed += 1
            elif worst_status == Submission.Status.ACCEPTED:
                worst_status = status

            if result.get("compile_output"):
                submission.error_output = result.get("compile_output") or ""
            elif result.get("stderr"):
                submission.error_output = result.get("stderr") or ""

        total = len(tests) or 1
        submission.score = round((passed / total) * 100)
        submission.status = Submission.Status.ACCEPTED if passed == total else worst_status
        submission.execution_time = max_time
        submission.memory_used = max_memory
        submission.judge_output = "\n".join(outputs)
    except Exception as exc:
        submission.status = Submission.Status.INTERNAL_ERROR
        submission.error_output = str(exc)
    finally:
        submission.judged_at = timezone.now()
        submission.save()
        update_progress(submission.student, submission.question.module)
    return submission


def update_progress(student, module):
    questions = Question.objects.filter(module=module, is_active=True)
    total = questions.count()
    attempted = questions.filter(submissions__student=student).distinct().count()
    completed = questions.filter(
        submissions__student=student,
        submissions__status=Submission.Status.ACCEPTED,
    ).distinct().count()
    percentage = (completed / total * 100) if total else 0
    progress, _ = Progress.objects.update_or_create(
        student=student,
        module=module,
        defaults={"attempted": attempted, "completed": completed, "percentage": percentage},
    )
    return progress


def student_progress(student):
    modules = Module.objects.filter(is_active=True).annotate(total=Count("questions", filter=Q(questions__is_active=True)))
    rows = []
    for module in modules:
        rows.append(update_progress(student, module))
    return rows


def overall_percentage(student):
    total = Question.objects.filter(is_active=True).count()
    if total == 0:
        return 0
    completed = Question.objects.filter(
        is_active=True,
        submissions__student=student,
        submissions__status=Submission.Status.ACCEPTED,
    ).distinct().count()
    return completed / total * 100


def certificate_eligible(student):
    pct = overall_percentage(student)
    mandatory_total = Question.objects.filter(is_active=True, is_mandatory=True).count()
    mandatory_done = Question.objects.filter(
        is_active=True,
        is_mandatory=True,
        submissions__student=student,
        submissions__status=Submission.Status.ACCEPTED,
    ).distinct().count()
    return pct >= settings.CERTIFICATE_THRESHOLD and mandatory_done == mandatory_total, pct


def generate_certificate(student):
    from weasyprint import HTML

    eligible, pct = certificate_eligible(student)
    if not eligible:
        return None

    semester = Certificate.current_semester_label()
    verification_hash = Certificate.make_hash(student, semester, pct)
    cert, created = Certificate.objects.get_or_create(
        verification_hash=verification_hash,
        defaults={
            "student": student,
            "semester": semester,
            "completion_percentage": pct,
        },
    )
    if not created and cert.pdf:
        return cert

    verify_url = f"{settings.SITE_BASE_URL}/verify/{verification_hash}/"
    qr = qrcode.make(verify_url)
    qr_buffer = BytesIO()
    qr.save(qr_buffer, format="PNG")
    cert.qr_code.save(f"{verification_hash}.png", ContentFile(qr_buffer.getvalue()), save=False)

    html = render_to_string(
        "certificates/certificate.html",
        {
            "student": student,
            "percentage": pct,
            "semester": semester,
            "issued_at": timezone.localtime(),
            "verify_url": verify_url,
            "certificate": cert,
            "site_name": settings.SITE_NAME,
        },
    )
    pdf_bytes = HTML(string=html, base_url=str(settings.BASE_DIR)).write_pdf()
    name_usn = student.usn or student.username
    cert.pdf.save(f"{name_usn}_{semester.replace(' ', '_')}.pdf", ContentFile(pdf_bytes), save=False)
    cert.save()
    return cert
