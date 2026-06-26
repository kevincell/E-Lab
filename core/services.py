from io import BytesIO
from difflib import SequenceMatcher
import random

import qrcode
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.db.models import Count, Q
from django.template.loader import render_to_string
from django.utils import timezone

from .models import AssignedQuestion, Attendance, Certificate, LabSession, Module, ModuleQuestionAssignment, Progress, Question, Submission
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


def similarity(a, b):
    return SequenceMatcher(None, a or "", b or "").ratio()


def check_plagiarism(submission):
    similar = []
    other_submissions = Submission.objects.filter(question=submission.question).exclude(pk=submission.pk)
    for other in other_submissions.select_related("student"):
        if similarity(submission.code, other.code) > 0.85:
            similar.append(other)
    return similar


def flag_plagiarism(submission):
    similar = check_plagiarism(submission)
    if not similar:
        return []

    labels = [f"#{other.pk} {other.student.display_name}" for other in similar[:10]]
    submission.plagiarism_flagged = True
    submission.plagiarism_notes = "Similar to: " + ", ".join(labels)
    submission.save(update_fields=["plagiarism_flagged", "plagiarism_notes"])
    return similar


def record_attendance(student, module):
    if not student.is_authenticated or student.role != student.Role.STUDENT:
        return None

    session, _ = LabSession.objects.get_or_create(date=timezone.localdate(), module=module)
    session.students_present.add(student)
    attendance = (
        Attendance.objects.filter(student=student, session=session, logout_time__isnull=True)
        .order_by("-login_time")
        .first()
    )
    if attendance:
        return attendance
    return Attendance.objects.create(student=student, session=session)


def close_open_attendance(student):
    if not student.is_authenticated:
        return

    now = timezone.now()
    rows = Attendance.objects.filter(student=student, logout_time__isnull=True)
    for row in rows:
        row.logout_time = now
        row.time_spent_minutes = max(1, round((now - row.login_time).total_seconds() / 60))
        row.save(update_fields=["logout_time", "time_spent_minutes"])


def student_performance_band(student):
    judged = Submission.objects.filter(student=student).exclude(status__in=[Submission.Status.PENDING, Submission.Status.RUNNING])
    total = judged.count()
    if not total:
        return "new"

    accepted = judged.filter(status=Submission.Status.ACCEPTED).count()
    avg_score = sum(judged.values_list("score", flat=True)) / total
    accept_rate = accepted / total
    if accept_rate >= 0.7 and avg_score >= 70:
        return "strong"
    if accept_rate >= 0.4 and avg_score >= 40:
        return "steady"
    return "support"


def choose_adaptive_questions(student, module, difficulty, count=5):
    questions = list(module.questions.filter(is_active=True, difficulty=difficulty).order_by("csv_level", "id"))
    rng = random.SystemRandom()
    rng.shuffle(questions)
    if len(questions) <= count:
        return questions

    accepted_ids = set(
        Submission.objects.filter(
            student=student,
            status=Submission.Status.ACCEPTED,
            question__module=module,
            question__difficulty=difficulty,
        ).values_list("question_id", flat=True)
    )
    unsolved = [question for question in questions if question.id not in accepted_ids]
    pool = unsolved if len(unsolved) >= count else unsolved + [question for question in questions if question.id in accepted_ids]

    band = student_performance_band(student)
    if band == "support":
        pool.sort(key=lambda question: (question.csv_level, rng.random()))
    elif band == "strong":
        pool.sort(key=lambda question: (-question.csv_level, rng.random()))
    else:
        rng.shuffle(pool)
    return pool[:count]


def sync_assignment_completion(assignment):
    accepted_ids = set(
        Submission.objects.filter(
            student=assignment.student,
            status=Submission.Status.ACCEPTED,
            question__assigned_slots__assignment=assignment,
        ).values_list("question_id", flat=True)
    )
    now = timezone.now()
    slots = list(assignment.assigned_questions.select_related("question"))
    changed = False

    for index, slot in enumerate(slots):
        if index == 0 and not slot.unlocked_at:
            slot.unlocked_at = now
            changed = True
        if slot.question_id in accepted_ids and not slot.completed_at:
            slot.completed_at = now
            changed = True
        if slot.completed_at and index + 1 < len(slots) and not slots[index + 1].unlocked_at:
            slots[index + 1].unlocked_at = now
            changed = True

    for slot in slots:
        if slot.pk and (slot.unlocked_at or slot.completed_at):
            slot.save(update_fields=["unlocked_at", "completed_at"])

    if slots and all(slot.completed_at for slot in slots) and not assignment.completed_at:
        assignment.completed_at = now
        assignment.save(update_fields=["completed_at"])
    elif changed and assignment.completed_at and not all(slot.completed_at for slot in slots):
        assignment.completed_at = None
        assignment.save(update_fields=["completed_at"])
    return slots


def get_or_create_module_assignment(student, module, difficulty=Question.Difficulty.EASY):
    assignment, created = ModuleQuestionAssignment.objects.get_or_create(
        student=student,
        module=module,
        difficulty=difficulty,
    )
    if created or not assignment.assigned_questions.exists():
        AssignedQuestion.objects.filter(assignment=assignment).delete()
        for index, question in enumerate(choose_adaptive_questions(student, module, difficulty), start=1):
            AssignedQuestion.objects.create(
                assignment=assignment,
                question=question,
                order=index,
                unlocked_at=timezone.now() if index == 1 else None,
            )
    sync_assignment_completion(assignment)
    return assignment


def current_unlocked_question(assignment):
    sync_assignment_completion(assignment)
    return (
        assignment.assigned_questions.filter(unlocked_at__isnull=False, completed_at__isnull=True)
        .select_related("question")
        .order_by("order")
        .first()
    )


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
        flag_plagiarism(submission)
        for assignment in ModuleQuestionAssignment.objects.filter(student=submission.student, module=submission.question.module):
            sync_assignment_completion(assignment)
        update_progress(submission.student, submission.question.module)
    return submission


def update_progress(student, module):
    questions = Question.objects.filter(module=module, is_active=True)
    total = questions.count()
    attempted = questions.filter(submissions__student=student).distinct().count()
    completed = questions.filter(submissions__student=student, submissions__status=Submission.Status.ACCEPTED).distinct().count()
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
    total = Question.objects.filter(module__is_active=True, is_active=True).count()
    if total == 0:
        return 0

    completed = (
        Submission.objects.filter(student=student, question__module__is_active=True, question__is_active=True, status=Submission.Status.ACCEPTED)
        .values_list("question_id", flat=True)
        .distinct()
        .count()
    )

    return completed / total * 100

def certificate_eligible(student):
    pct = overall_percentage(student)
    mandatory_questions = Question.objects.filter(module__is_active=True, is_active=True, is_mandatory=True)
    mandatory_total = mandatory_questions.count()
    mandatory_done = mandatory_questions.filter(
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
    notify_certificate(student, cert)
    return cert


def notify_certificate(student, certificate):
    if not student.email:
        return

    send_mail(
        subject=f"{settings.SITE_NAME} - Certificate Generated",
        message=f"Congratulations! Your certificate for {certificate.semester} is ready.",
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
        recipient_list=[student.email],
        fail_silently=True,
    )
