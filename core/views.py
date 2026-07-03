import csv
import io
import os
import re
import subprocess

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.db import connection
from django.db.models import Count, Q, Sum, Value
from django.db.models.functions import Coalesce
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import CreateView
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .forms import CSVQuestionUploadForm, ModuleForm, QuestionForm, QuickTestCaseForm, StudentSignUpForm, SubmissionForm, TestCaseForm
from .models import AssignedQuestion, Certificate, CertificateRequest, LabSession, Module, ModuleQuestionAssignment, Notification, Progress, Question, Submission, TestCase, User
from .sandbox import run_c_code
from .serializers import ProgressSerializer, QuestionSerializer, SubmissionSerializer
from .services import (
    certificate_eligible,
    close_open_attendance,
    current_unlocked_question,
    generate_certificate,
    get_or_create_module_assignment,
    notify_faculty_of_eligible_student,
    notify_hod_of_cert_request,
    notify_student_of_cert_decision,
    overall_percentage,
    record_attendance,
    sync_assignment_completion,
    student_progress,
    update_progress,
)
from .tasks import evaluate_submission_task


class AppLoginView(LoginView):
    template_name = "registration/login.html"

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated and user.role == User.Role.HOD:
            return reverse_lazy("role_select")
        return super().get_success_url() or reverse_lazy("dashboard")


class AppLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        close_open_attendance(request.user)
        if "active_role" in request.session:
            del request.session["active_role"]
        return super().dispatch(request, *args, **kwargs)


class SignUpView(CreateView):
    form_class = StudentSignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


def faculty_required(user):
    if not user.is_authenticated or not user.is_faculty_like:
        raise PermissionDenied


@login_required
def dashboard(request):
    if request.user.role == User.Role.ADMIN:
        return redirect("admin:index")

    # HoD with active role "hod" goes to HoD dashboard
    if request.user.role == User.Role.HOD:
        active_role = request.session.get("active_role")
        if active_role == "hod":
            return redirect("hod_dashboard")
        elif active_role != "faculty":
            return redirect("role_select")

    if request.user.is_faculty_like:
        modules = Module.objects.annotate(
            question_count=Count("questions"),
            active_question_count=Count("questions", filter=Q(questions__is_active=True)),
        )
        selected_category = request.GET.get("category") or "overall"
        selected_sort = request.GET.get("sort") or "rank"
        if selected_sort not in {"rank", "usn"}:
            selected_sort = "rank"

        progress_modules = list(modules.order_by("order", "name"))
        progress_students_qs = (
            User.objects.filter(is_staff=False, is_superuser=False)
            .exclude(role__in=[User.Role.FACULTY, User.Role.ADMIN])
        )
        selected_module = None
        if selected_category != "overall":
            try:
                selected_module_id = int(selected_category)
            except (TypeError, ValueError):
                selected_category = "overall"
            else:
                selected_module = next((module for module in progress_modules if module.id == selected_module_id), None)
                if selected_module is None:
                    selected_category = "overall"

        if selected_module:
            progress_total = min(15, selected_module.question_count)
            progress_students = progress_students_qs.annotate(
                attempted_count=Count(
                    "submissions__question",
                    filter=Q(
                        submissions__question__module=selected_module,
                    ),
                    distinct=True,
                ),
                completed_count=Count(
                    "submissions__question",
                    filter=Q(
                        submissions__question__module=selected_module,
                        submissions__status=Submission.Status.ACCEPTED,
                    ),
                    distinct=True,
                ),
            )
            selected_category_label = selected_module.name
        else:
            progress_total = sum(min(15, module.question_count) for module in progress_modules)
            progress_students = progress_students_qs.annotate(
                attempted_count=Count(
                    "submissions__question",
                    distinct=True,
                ),
                completed_count=Count(
                    "submissions__question",
                    filter=Q(submissions__status=Submission.Status.ACCEPTED),
                    distinct=True,
                ),
            )
            selected_category_label = "Overall Progress"

        progress_tracker = []
        for student in progress_students:
            attempted = min(student.attempted_count, progress_total)
            completed = min(student.completed_count, progress_total)
            percentage = (completed / progress_total * 100) if progress_total else 0
            progress_tracker.append(
                {
                    "student": student,
                    "student_usn": student.usn or student.username,
                    "attempted": attempted,
                    "completed": completed,
                    "total": progress_total,
                    "percentage": percentage,
                }
            )

        ranked_tracker = sorted(
            progress_tracker,
            key=lambda row: (
                -row["percentage"],
                -row["completed"],
                -row["attempted"],
                row["student_usn"].lower(),
                row["student"].username.lower(),
            ),
        )
        for index, row in enumerate(ranked_tracker, start=1):
            row["rank"] = index

        if selected_sort == "usn":
            progress_tracker = sorted(
                ranked_tracker,
                key=lambda row: (row["student_usn"].lower(), row["student"].username.lower()),
            )
        else:
            progress_tracker = ranked_tracker

        recent = Submission.objects.select_related("student", "question")[:12]
        recent_sessions = LabSession.objects.select_related("module").prefetch_related("attendance_rows__student")[:6]
        flagged_submissions = Submission.objects.filter(plagiarism_flagged=True).select_related("student", "question")[:8]
        students = progress_students_qs.count()
        return render(
            request,
            "faculty/dashboard.html",
            {
                "modules": modules,
                "recent_submissions": recent,
                "recent_sessions": recent_sessions,
                "flagged_submissions": flagged_submissions,
                "students": students,
                "questions": Question.objects.count(),
                "progress_tracker": progress_tracker,
                "progress_modules": progress_modules,
                "selected_category": selected_category,
                "selected_category_label": selected_category_label,
                "selected_sort": selected_sort,
                "progress_total": progress_total,
            },
        )

    progress_rows = student_progress(request.user)
    modules = Module.objects.filter(is_active=True).prefetch_related("questions")
    progress_by_module = {row.module_id: row for row in progress_rows}
    user_submissions = Submission.objects.filter(student=request.user).values("question_id", "status")
    question_status_map = {}
    for sub in user_submissions:
        qid = sub["question_id"]
        st = sub["status"]
        if qid not in question_status_map:
            question_status_map[qid] = set()
        question_status_map[qid].add(st)

    module_cards = []
    for module in modules:
        progress = progress_by_module.get(module.id)
        module_questions = module.questions.filter(is_active=True)
        if request.user.is_faculty_like:
            module_total = module_questions.count()
            module_completed = module_questions.filter(
                submissions__student=request.user,
                submissions__status=Submission.Status.ACCEPTED,
            ).distinct().count()
            questions_for_dots = list(module_questions)
        else:
            module_total = min(15, module_questions.count())
            assigned_qs = AssignedQuestion.objects.filter(
                assignment__student=request.user, assignment__module=module
            )
            if assigned_qs.exists():
                module_completed = assigned_qs.filter(completed_at__isnull=False).count()
                questions_for_dots = [aq.question for aq in assigned_qs.select_related("question")]
            else:
                module_completed = module_questions.filter(
                    submissions__student=request.user,
                    submissions__status=Submission.Status.ACCEPTED,
                ).distinct().count()
                module_completed = min(module_completed, module_total)
                questions_for_dots = list(module_questions[:module_total])

        question_statuses = []
        for q in questions_for_dots:
            st_set = question_status_map.get(q.id, set())
            if Submission.Status.ACCEPTED in st_set:
                question_statuses.append("completed")
            elif any(
                s in st_set
                for s in [
                    Submission.Status.WRONG_ANSWER,
                    Submission.Status.TLE,
                    Submission.Status.RUNTIME_ERROR,
                    Submission.Status.COMPILE_ERROR,
                    Submission.Status.INTERNAL_ERROR,
                ]
            ):
                question_statuses.append("failed")
            else:
                question_statuses.append("pending")
        if not question_statuses and module_total > 0:
            question_statuses = ["pending"] * module_total

        module_percentage = (module_completed / module_total * 100) if module_total else 0
        module_cards.append(
            {
                "module": module,
                "progress": progress,
                "percentage": module_percentage,
                "module_total": module_total,
                "module_completed": module_completed,
                "completed": module_total > 0 and module_completed == module_total,
                "question_statuses": question_statuses,
            }
        )
    pct = overall_percentage(request.user)
    dashboard_questions = Question.objects.filter(module__is_active=True, is_active=True)
    if request.user.is_faculty_like:
        questions_total = dashboard_questions.count()
        completed_total = dashboard_questions.filter(
            submissions__student=request.user,
            submissions__status=Submission.Status.ACCEPTED,
        ).distinct().count()
    else:
        questions_total = sum(card["module_total"] for card in module_cards)
        completed_total = sum(card["module_completed"] for card in module_cards)
    eligible, _ = certificate_eligible(request.user)
    certificates = request.user.certificates.all()

    # Enhanced data for Ecosystem UI
    leaderboard_qs = (
        User.objects.filter(role=User.Role.STUDENT)
        .annotate(
            total_score=Coalesce(Sum("submissions__score"), Value(0)),
            problems_solved=Count("submissions__question", filter=Q(submissions__status=Submission.Status.ACCEPTED), distinct=True),
        )
    )

    # Efficient rank calculation
    current_user_stats = leaderboard_qs.get(id=request.user.id)
    user_rank = leaderboard_qs.filter(
        Q(total_score__gt=current_user_stats.total_score) |
        Q(total_score=current_user_stats.total_score, problems_solved__gt=current_user_stats.problems_solved) |
        Q(total_score=current_user_stats.total_score, problems_solved=current_user_stats.problems_solved, username__lt=current_user_stats.username)
    ).count() + 1

    global_leaderboard = leaderboard_qs.order_by("-total_score", "-problems_solved", "username")[:20]
    recent_activity = Submission.objects.filter(student=request.user).select_related("question")[:10]
    live_flags_count = Submission.objects.filter(student=request.user, plagiarism_flagged=True).count()

    return render(
        request,
        "student/dashboard.html",
        {
            "modules": modules,
            "module_cards": module_cards,
            "progress_rows": progress_rows,
            "overall_percentage": pct,
            "questions_total": questions_total,
            "completed_total": completed_total,
            "not_attempted_total": max(questions_total - completed_total, 0),
            "certificate_eligible": eligible,
            "certificates": certificates,
            "user_rank": user_rank,
            "global_leaderboard": global_leaderboard,
            "recent_activity": recent_activity,
            "live_flags_count": live_flags_count,
        },
    )


@login_required
def module_detail(request, module_id):
    module = get_object_or_404(Module, pk=module_id, is_active=True)
    record_attendance(request.user, module)
    level_cards = []
    for value, label in Question.Difficulty.choices:
        questions = module.questions.filter(is_active=True, difficulty=value)
        if request.user.is_faculty_like:
            total = questions.count()
            completed = questions.filter(
                submissions__student=request.user,
                submissions__status=Submission.Status.ACCEPTED,
            ).distinct().count()
        else:
            assignment = ModuleQuestionAssignment.objects.filter(
                student=request.user, module=module, difficulty=value
            ).first()
            if assignment:
                total = assignment.assigned_questions.count()
                completed = assignment.assigned_questions.filter(completed_at__isnull=False).count()
            else:
                total = min(5, questions.count())
                completed = questions.filter(
                    submissions__student=request.user,
                    submissions__status=Submission.Status.ACCEPTED,
                ).distinct().count()
                completed = min(completed, total)

        level_cards.append(
            {
                "value": value,
                "label": label,
                "total": total,
                "completed": completed,
                "percentage": (completed / total * 100) if total else 0,
            }
        )
    return render(request, "student/module_detail.html", {"module": module, "level_cards": level_cards})


@login_required
def module_level_detail(request, module_id, difficulty):
    module = get_object_or_404(Module, pk=module_id, is_active=True)
    valid_difficulties = {value for value, _ in Question.Difficulty.choices}
    if difficulty not in valid_difficulties:
        raise PermissionDenied
    record_attendance(request.user, module)
    if request.user.is_faculty_like:
        questions = module.questions.filter(is_active=True, difficulty=difficulty)
        accepted_ids = set()
        assigned_slots = []
        current_slot = None
    else:
        assignment = get_or_create_module_assignment(request.user, module, difficulty)
        assigned_slots = sync_assignment_completion(assignment)
        questions = [slot.question for slot in assigned_slots]
        current_slot = current_unlocked_question(assignment)
        accepted_ids = {slot.question_id for slot in assigned_slots if slot.completed_at}
    difficulty_label = dict(Question.Difficulty.choices).get(difficulty, difficulty.title())
    return render(
        request,
        "student/module_level_detail.html",
        {
            "module": module,
            "difficulty": difficulty,
            "difficulty_label": difficulty_label,
            "questions": questions,
            "assigned_slots": assigned_slots,
            "current_slot": current_slot,
            "accepted_ids": accepted_ids,
        },
    )


@login_required
def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id, is_active=True)
    if not request.user.is_faculty_like:
        assignment = get_or_create_module_assignment(request.user, question.module, question.difficulty)
        slot = assignment.assigned_questions.filter(question=question).first()
        if not slot or not slot.unlocked_at:
            messages.error(request, "Solve your current unlocked question before opening the next one.")
            return redirect("module_level_detail", question.module_id, question.difficulty)
    record_attendance(request.user, question.module)
    latest = Submission.objects.filter(student=request.user, question=question).first()
    initial = {"code": latest.code if latest else question.starter_code}
    form = SubmissionForm(request.POST or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        if not can_submit(request.user, question):
            messages.error(request, "Please wait 30 seconds before submitting again.")
            return redirect("question_detail", question.pk)
        submission = form.save(commit=False)
        submission.student = request.user
        submission.question = question
        submission.language_id = question.language_id
        submission.save()
        evaluate_submission_task.delay(submission.pk)
        messages.success(request, "Submission queued. We'll take you to the results shortly.")
        return redirect("submission_detail", submission.pk)

    return render(
        request,
        "student/question_detail.html",
        {"question": question, "form": form, "latest_submission": latest},
    )


@login_required
def submission_detail(request, submission_id):
    submission = get_object_or_404(Submission.objects.select_related("question"), pk=submission_id)
    if submission.student != request.user and not request.user.is_faculty_like:
        raise PermissionDenied
    return render(request, "student/submission_detail.html", {"submission": submission})


@login_required
def manual_accept_submission(request, submission_id):
    faculty_required(request.user)
    if request.method != "POST":
        raise PermissionDenied
    submission = get_object_or_404(Submission.objects.select_related("question", "student"), pk=submission_id)
    submission.status = Submission.Status.ACCEPTED
    submission.score = 100
    submission.manually_graded = True
    submission.graded_by = request.user
    submission.judged_at = timezone.now()
    submission.save(update_fields=["status", "score", "manually_graded", "graded_by", "judged_at"])
    for assignment in submission.student.module_assignments.filter(module=submission.question.module):
        sync_assignment_completion(assignment)
    update_progress(submission.student, submission.question.module)
    messages.success(request, "Submission manually marked as accepted.")
    return redirect("submission_detail", submission.pk)


@login_required
def certificate_create(request):
    cert = generate_certificate(request.user)
    if not cert:
        messages.error(request, "Certificate is not available yet. Complete the required modules first.")
        return redirect("dashboard")
    messages.success(request, "Certificate generated.")
    return redirect("certificate_detail", cert.pk)


@login_required
def certificate_detail(request, certificate_id):
    cert = get_object_or_404(Certificate, pk=certificate_id)
    if cert.student != request.user and not request.user.is_faculty_like:
        raise PermissionDenied
    return render(request, "certificates/detail.html", {"certificate": cert})


def certificate_verify(request, verification_hash):
    cert = get_object_or_404(Certificate.objects.select_related("student"), verification_hash=verification_hash)
    return render(request, "certificates/verify.html", {"certificate": cert})


@login_required
def leaderboard(request):
    students = (
        User.objects.filter(role=User.Role.STUDENT)
        .annotate(
            total_score=Coalesce(Sum("submissions__score"), Value(0)),
            problems_solved=Count("submissions__question", filter=Q(submissions__status=Submission.Status.ACCEPTED), distinct=True),
        )
        .order_by("-total_score", "-problems_solved", "username")[:50]
    )
    return render(request, "student/leaderboard.html", {"students": students})


@login_required
def export_progress(request):
    faculty_required(request.user)
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="progress.csv"'
    writer = csv.writer(response)
    writer.writerow(["USN", "Name", "Module", "Attempted", "Completed", "Percentage"])
    rows = Progress.objects.select_related("student", "module").order_by("student__usn", "module__order")
    for row in rows:
        writer.writerow(
            [
                row.student.usn,
                row.student.display_name,
                row.module.name,
                row.attempted,
                row.completed,
                f"{row.percentage:.2f}",
            ]
        )
    return response


@login_required
def attendance_report(request):
    faculty_required(request.user)
    sessions = LabSession.objects.select_related("module").prefetch_related("attendance_rows__student")[:30]
    return render(request, "faculty/attendance.html", {"sessions": sessions})


def can_submit(student, question):
    key = f"submit:{student.id}:{question.id}"
    last = cache.get(key)
    now = timezone.now()
    if last and (now - last).total_seconds() < 30:
        return False
    cache.set(key, now, 30)
    return True


def check_database():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return True
    except Exception:
        return False


def check_sandbox():
    try:
        result = subprocess.run(
            ["docker", "image", "inspect", "elab-sandbox"],
            capture_output=True,
            text=True,
            timeout=3,
        )
        return result.returncode == 0
    except Exception:
        return False


def health_check(request):
    database_ok = check_database()
    sandbox_ok = check_sandbox()
    status = 200 if database_ok and sandbox_ok else 503
    return JsonResponse(
        {
            "status": "ok" if status == 200 else "error",
            "timestamp": timezone.now().isoformat(),
            "database": "connected" if database_ok else "error",
            "sandbox": "ready" if sandbox_ok else "error",
        },
        status=status,
    )


@login_required
@require_POST
def run_code(request):
    import json
    data = json.loads(request.body)
    question_id = data.get("question")
    code = data.get("code")
    
    question = get_object_or_404(Question, id=question_id, is_active=True)
    test_cases = question.test_cases.filter(is_sample=True).order_by("order")
    
    if not test_cases:
        test_cases = [
            TestCase(
                stdin=question.sample_input,
                expected_output=question.sample_output,
            )
        ]
    
    results = []
    for test in test_cases:
        run_result = run_c_code(
            source_code=code,
            stdin=test.stdin or "",
            expected_output=test.expected_output or "",
            time_limit=question.time_limit,
            memory_limit_kb=question.memory_limit_kb,
        )
        passed = run_result.get("status_id") == 3
        results.append({
            "stdin": test.stdin or "",
            "expected": test.expected_output or "",
            "actual": run_result.get("stdout", ""),
            "passed": passed,
            "status": run_result.get("status", "Unknown"),
        })
    
    return JsonResponse({
        "tests": results,
    })


@login_required
def faculty_module_form(request, module_id=None):
    faculty_required(request.user)
    module = get_object_or_404(Module, pk=module_id) if module_id else None
    form = ModuleForm(request.POST or None, instance=module)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Module saved.")
        return redirect("dashboard")
    return render(request, "faculty/form.html", {"form": form, "title": "Module", "module": module})


@login_required
def faculty_module_delete(request, module_id):
    faculty_required(request.user)
    if request.method != "POST":
        raise PermissionDenied
    module = get_object_or_404(Module, pk=module_id)
    name = module.name
    module.delete()
    messages.success(request, f"Deleted module {name}.")
    return redirect("dashboard")


@login_required
def faculty_question_bank(request, module_id=None):
    faculty_required(request.user)
    modules = Module.objects.annotate(
        question_count=Count("questions"),
        active_question_count=Count("questions", filter=Q(questions__is_active=True)),
    ).order_by("order")

    selected_module = None
    questions_by_difficulty = {}
    stats = {}

    if not module_id and modules.exists():
        module_id = modules.first().id

    if module_id:
        selected_module = get_object_or_404(Module, pk=module_id)
        all_questions = list(
            selected_module.questions
            .annotate(test_count=Count("test_cases"))
            .order_by("difficulty", "csv_level", "title")
        )
        for diff_value, diff_label in Question.Difficulty.choices:
            qs = [q for q in all_questions if q.difficulty == diff_value]
            questions_by_difficulty[diff_label] = qs

        stats = {
            "total": len(all_questions),
            "easy": len([q for q in all_questions if q.difficulty == Question.Difficulty.EASY]),
            "medium": len([q for q in all_questions if q.difficulty == Question.Difficulty.MEDIUM]),
            "hard": len([q for q in all_questions if q.difficulty == Question.Difficulty.HARD]),
            "mandatory": len([q for q in all_questions if q.is_mandatory]),
        }

    return render(
        request,
        "faculty/question_bank.html",
        {
            "modules": modules,
            "selected_module": selected_module,
            "questions_by_difficulty": questions_by_difficulty,
            "stats": stats,
        },
    )


def module_name_from_csv(filename):
    filename = os.path.basename(filename)
    stem = filename.rsplit(".", 1)[0]
    match = re.match(r"Module(\d+)_(.+)", stem, re.IGNORECASE)
    if not match:
        name = re.sub(r"[_\s]+(?:Full|Levels)$", "", stem, flags=re.IGNORECASE)
        return name.replace("_", " ").strip(), 1
    order = int(match.group(1))
    raw_name = re.sub(r"[_\s]+(?:Full|Levels)$", "", match.group(2), flags=re.IGNORECASE)
    name = raw_name.replace("_", " ").replace("IO", "I/O").strip()
    name = name.replace("Operators Expressions", "Operators & Expressions")
    name = name.replace("Conditionals Loops", "Conditionals & Loops")
    return name, order


def difficulty_from_csv(value):
    value = (value or "").strip().lower()
    if value == "medium":
        return Question.Difficulty.MEDIUM
    if value in {"hard", "expert"}:
        return Question.Difficulty.HARD
    return Question.Difficulty.EASY


def question_description_from_row(row, module):
    explicit = (row.get("Problem_Statement") or row.get("Description") or "").strip()
    if explicit:
        return explicit

    topic = row.get("Topic", "").strip()
    level = row.get("Level", "").strip()
    level_range = row.get("Level_Range", "").strip()
    difficulty = row.get("Difficulty", "").strip()
    return (
        f"Topic: {topic}\n"
        f"Module: {module.name}\n"
        f"Level: {level} ({level_range})\n"
        f"Difficulty: {difficulty}\n\n"
        "Write a C program for this exercise. Read all input from stdin and print only the exact expected output.\n\n"
        "Faculty note: replace this scaffold with the complete problem statement, input format, output format, "
        "constraints, and examples before making the question live."
    )


def starter_code_for_csv_question(row=None):
    explicit = ((row or {}).get("Starter_Code") or "").strip()
    if explicit:
        return explicit
    return (
        "#include <stdio.h>\n\n"
        "int main(void)\n"
        "{\n"
        "    /* Read from stdin. Do not print prompts unless required. */\n"
        "    return 0;\n"
        "}\n"
    )


def bool_from_csv(value, default=False):
    value = str(value or "").strip().lower()
    if value in {"1", "true", "yes", "y", "active"}:
        return True
    if value in {"0", "false", "no", "n", "inactive", "draft"}:
        return False
    return default


def row_test_cases(row):
    cases = []
    for index in range(1, 21):
        stdin = row.get(f"Test{index}_Input")
        expected = row.get(f"Test{index}_Output")
        if expected is None:
            expected = row.get(f"Test{index}_Expected_Output")
        if expected is None:
            continue
        if str(stdin or "").strip() == "" and str(expected or "").strip() == "":
            continue
        cases.append((index, stdin or "", expected or ""))
    return cases


def import_question_csv(file_obj, faculty):
    module_name, order = module_name_from_csv(file_obj.name)
    module, _ = Module.objects.update_or_create(
        name=module_name,
        defaults={
            "description": f"Imported question bank for {module_name}.",
            "level": order,
            "order": order,
            "is_active": True,
        },
    )

    decoded = file_obj.read().decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(decoded))
    required = {"Question_ID", "Topic", "Level", "Difficulty"}
    missing = required.difference(reader.fieldnames or [])
    if missing:
        raise ValueError(f"{file_obj.name}: missing columns {', '.join(sorted(missing))}")

    created = 0
    updated = 0
    active = 0
    test_cases = 0
    imported_slugs = []
    replace_bank = "_levels" in file_obj.name.lower()
    for index, row in enumerate(reader, start=1):
        question_id = (row.get("Question_ID") or f"Q{index:03d}").strip()
        topic = (row.get("Topic") or "Question").strip()
        level = (row.get("Level") or "1").strip()
        title = (row.get("Title") or f"{question_id} - {topic} (Level {level})").strip()
        slug = slugify(f"{question_id}-{topic}-level-{level}")[:180]
        imported_slugs.append(slug)
        tests = row_test_cases(row)
        active_default = bool(tests) and bool((row.get("Problem_Statement") or row.get("Description") or "").strip())
        obj, was_created = Question.objects.update_or_create(
            module=module,
            slug=slug,
            defaults={
                "title": title,
                "description": question_description_from_row(row, module),
                "difficulty": difficulty_from_csv(row.get("Difficulty")),
                "csv_level": int(row.get("Level") or 1),
                "level_range": (row.get("Level_Range") or "").strip(),
                "starter_code": starter_code_for_csv_question(row),
                "language_id": 50,
                "time_limit": float(row.get("Time_Limit") or 2.0),
                "memory_limit_kb": int(row.get("Memory_Limit_KB") or 128000),
                "is_mandatory": bool_from_csv(row.get("Is_Mandatory"), default=False),
                "is_active": bool_from_csv(row.get("Is_Active"), default=active_default),
                "created_by": faculty,
            },
        )
        for test_order, stdin, expected in tests:
            TestCase.objects.update_or_create(
                question=obj,
                order=test_order,
                defaults={
                    "stdin": stdin,
                    "expected_output": expected,
                    "is_sample": test_order == 1,
                },
            )
        if tests:
            TestCase.objects.filter(question=obj).exclude(order__in=[case[0] for case in tests]).delete()
        test_cases += len(tests)
        if obj.is_active:
            active += 1
        if was_created:
            created += 1
        else:
            updated += 1

    stale_deleted = 0
    if test_cases:
        stale_qs = (
            Question.objects.filter(module=module, is_active=False, description__startswith="Topic:")
            .annotate(test_count=Count("test_cases"))
            .filter(test_count=0)
            .exclude(slug__in=imported_slugs)
        )
        stale_deleted, _ = stale_qs.delete()

    replaced_deleted = 0
    assignments_reset = 0
    if replace_bank:
        replaced_deleted, _ = Question.objects.filter(module=module).exclude(slug__in=imported_slugs).delete()
        assignments_reset, _ = ModuleQuestionAssignment.objects.filter(module=module).delete()

    return {
        "module": module,
        "created": created,
        "updated": updated,
        "active": active,
        "test_cases": test_cases,
        "stale_deleted": stale_deleted,
        "replaced_deleted": replaced_deleted,
        "assignments_reset": assignments_reset,
    }


@login_required
def faculty_question_upload(request):
    faculty_required(request.user)
    form = CSVQuestionUploadForm(request.POST or None, request.FILES or None)
    results = []
    if request.method == "POST" and form.is_valid():
        for file_obj in form.cleaned_data["files"]:
            try:
                results.append(import_question_csv(file_obj, request.user))
            except Exception as exc:
                messages.error(request, str(exc))
        if results:
            total_created = sum(row["created"] for row in results)
            total_updated = sum(row["updated"] for row in results)
            total_active = sum(row["active"] for row in results)
            total_tests = sum(row["test_cases"] for row in results)
            total_deleted = sum(row["stale_deleted"] for row in results)
            total_replaced = sum(row["replaced_deleted"] for row in results)
            total_reset = sum(row["assignments_reset"] for row in results)
            messages.success(
                request,
                f"Imported {total_created} new questions, updated {total_updated}, activated {total_active}, synced {total_tests} test cases, removed {total_deleted} stale drafts, replaced {total_replaced} old bank questions, and reset {total_reset} assignments.",
            )
    return render(request, "faculty/question_upload.html", {"form": form, "results": results})


@login_required
def faculty_question_form(request, question_id=None):
    faculty_required(request.user)
    question = get_object_or_404(Question, pk=question_id) if question_id else None
    is_test_post = request.method == "POST" and request.POST.get("action") == "add_test"
    question_data = request.POST if request.method == "POST" and not is_test_post else None
    test_data = request.POST if is_test_post else None
    form = QuestionForm(question_data, instance=question)
    test_form = QuickTestCaseForm(test_data, initial={"order": 2})

    if is_test_post:
        if not question:
            messages.error(request, "Save the question before adding hidden tests.")
            return redirect("faculty_question_new")
        if test_form.is_valid():
            test = test_form.save(commit=False)
            test.question = question
            test.save()
            messages.success(request, "Test case added.")
            return redirect("faculty_question_edit", question.pk)
    elif request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        if not obj.created_by_id:
            obj.created_by = request.user
        obj.save()
        if obj.sample_output:
            TestCase.objects.update_or_create(
                question=obj,
                is_sample=True,
                order=1,
                defaults={"stdin": obj.sample_input, "expected_output": obj.sample_output},
            )
        messages.success(request, "Question saved.")
        return redirect("faculty_question_edit", obj.pk)
    tests = question.test_cases.all() if question else []
    return render(
        request,
        "faculty/question_form.html",
        {"form": form, "question": question, "tests": tests, "test_form": test_form},
    )


@login_required
def faculty_testcase_form(request, question_id):
    faculty_required(request.user)
    question = get_object_or_404(Question, pk=question_id)
    form = TestCaseForm(request.POST or None, initial={"question": question})
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Test case added.")
        return redirect("faculty_question_edit", question.pk)
    return render(request, "faculty/form.html", {"form": form, "title": "Test case"})


# =========================================================
#   Role Selection (HoD dual-login)
# =========================================================
@login_required
def role_select(request):
    if request.user.role != User.Role.HOD:
        return redirect("dashboard")

    if request.method == "POST":
        chosen = request.POST.get("role", "faculty")
        if chosen in ("hod", "faculty"):
            request.session["active_role"] = chosen
        if chosen == "hod":
            return redirect("hod_dashboard")
        return redirect("dashboard")

    return render(request, "registration/role_select.html")


# =========================================================
#   HoD Dashboard
# =========================================================
@login_required
def hod_dashboard(request):
    if request.user.role != User.Role.HOD or request.session.get("active_role") != "hod":
        return redirect("dashboard")

    pending_requests = CertificateRequest.objects.filter(
        status=CertificateRequest.Status.PENDING_HOD
    ).select_related("student", "requested_by_faculty").order_by("-updated_at")

    approved_count = CertificateRequest.objects.filter(status=CertificateRequest.Status.APPROVED).count()
    rejected_count = CertificateRequest.objects.filter(status=CertificateRequest.Status.REJECTED).count()
    total_students = User.objects.filter(role=User.Role.STUDENT).count()

    recent_decisions = CertificateRequest.objects.filter(
        status__in=[CertificateRequest.Status.APPROVED, CertificateRequest.Status.REJECTED]
    ).select_related("student", "requested_by_faculty", "approved_by_hod").order_by("-updated_at")[:10]

    return render(request, "hod/dashboard.html", {
        "pending_requests": pending_requests,
        "approved_count": approved_count,
        "rejected_count": rejected_count,
        "total_students": total_students,
        "recent_decisions": recent_decisions,
    })


# =========================================================
#   HoD Review Certificate Request
# =========================================================
@login_required
def hod_review_request(request, request_id):
    if request.user.role != User.Role.HOD or request.session.get("active_role") != "hod":
        return redirect("dashboard")

    cert_req = get_object_or_404(
        CertificateRequest.objects.select_related("student", "requested_by_faculty"),
        pk=request_id,
    )
    student = cert_req.student

    # Get full student activity
    modules = Module.objects.filter(is_active=True).prefetch_related("questions")
    module_progress = []
    for module in modules:
        total_q = module.questions.filter(is_active=True).count()
        solved = module.questions.filter(
            is_active=True,
            submissions__student=student,
            submissions__status=Submission.Status.ACCEPTED,
        ).distinct().count()
        pct = (solved / total_q * 100) if total_q else 0
        module_progress.append({
            "module": module,
            "total": total_q,
            "solved": solved,
            "percentage": pct,
        })

    recent_submissions = Submission.objects.filter(
        student=student
    ).select_related("question", "question__module").order_by("-submitted_at")[:30]

    pct = overall_percentage(student)

    return render(request, "hod/review_request.html", {
        "cert_req": cert_req,
        "student": student,
        "module_progress": module_progress,
        "recent_submissions": recent_submissions,
        "overall_pct": pct,
    })


# =========================================================
#   HoD Approve / Reject Certificate
# =========================================================
@login_required
@require_POST
def hod_approve_certificate(request, request_id):
    if request.user.role != User.Role.HOD or request.session.get("active_role") != "hod":
        raise PermissionDenied

    cert_req = get_object_or_404(CertificateRequest, pk=request_id, status=CertificateRequest.Status.PENDING_HOD)
    action = request.POST.get("action")
    notes = request.POST.get("notes", "").strip()

    if action == "approve":
        cert_req.status = CertificateRequest.Status.APPROVED
        cert_req.approved_by_hod = request.user
        cert_req.hod_notes = notes
        cert_req.save()
        # Auto-generate the certificate
        cert = generate_certificate(cert_req.student)
        notify_student_of_cert_decision(cert_req)
        messages.success(request, f"Certificate approved for {cert_req.student.display_name}.")
    elif action == "reject":
        cert_req.status = CertificateRequest.Status.REJECTED
        cert_req.approved_by_hod = request.user
        cert_req.hod_notes = notes
        cert_req.save()
        notify_student_of_cert_decision(cert_req)
        messages.info(request, f"Certificate request rejected for {cert_req.student.display_name}.")

    return redirect("hod_dashboard")


# =========================================================
#   Faculty Certificate Requests Page
# =========================================================
@login_required
def faculty_cert_requests(request):
    faculty_required(request.user)

    # Find eligible students
    all_students = User.objects.filter(role=User.Role.STUDENT)
    eligible_students = []
    for student in all_students:
        is_eligible, pct = certificate_eligible(student)
        if is_eligible:
            existing_req = CertificateRequest.objects.filter(student=student).order_by("-updated_at").first()
            eligible_students.append({
                "student": student,
                "percentage": pct,
                "existing_request": existing_req,
            })

    # Requests that this faculty has sent
    my_requests = CertificateRequest.objects.filter(
        requested_by_faculty=request.user
    ).select_related("student", "approved_by_hod").order_by("-updated_at")[:20]

    return render(request, "faculty/cert_requests.html", {
        "eligible_students": eligible_students,
        "my_requests": my_requests,
    })


# =========================================================
#   Faculty Send Certificate Request to HoD
# =========================================================
@login_required
@require_POST
def faculty_send_cert_request(request, student_id):
    faculty_required(request.user)

    student = get_object_or_404(User, pk=student_id, role=User.Role.STUDENT)
    is_eligible, pct = certificate_eligible(student)
    if not is_eligible:
        messages.error(request, f"{student.display_name} is not yet eligible for a certificate.")
        return redirect("faculty_cert_requests")

    # Check for existing pending request
    existing = CertificateRequest.objects.filter(
        student=student,
        status__in=[CertificateRequest.Status.PENDING_HOD, CertificateRequest.Status.APPROVED],
    ).first()
    if existing:
        messages.warning(request, f"A request for {student.display_name} already exists ({existing.get_status_display()}).")
        return redirect("faculty_cert_requests")

    notes = request.POST.get("notes", "").strip()
    cert_req = CertificateRequest.objects.create(
        student=student,
        requested_by_faculty=request.user,
        status=CertificateRequest.Status.PENDING_HOD,
        faculty_notes=notes,
        completion_percentage=pct,
    )
    notify_hod_of_cert_request(cert_req)
    messages.success(request, f"Approval request sent to HoD for {student.display_name}.")
    return redirect("faculty_cert_requests")


# =========================================================
#   Notifications
# =========================================================
@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by("-created_at")[:50]
    return render(request, "notifications/list.html", {"notifications": notifications})


@login_required
@require_POST
def notification_mark_read(request, notification_id):
    notif = get_object_or_404(Notification, pk=notification_id, recipient=request.user)
    notif.is_read = True
    notif.save(update_fields=["is_read"])
    return redirect("notifications_list")


@login_required
@require_POST
def notifications_mark_all_read(request):
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return redirect("notifications_list")


class SubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Submission.objects.select_related("question", "student")
        if self.request.user.is_faculty_like:
            return qs
        return qs.filter(student=self.request.user)

    def create(self, request, *args, **kwargs):
        print("DEBUG: Request data:", request.data)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        print("DEBUG: Validated data:", serializer.validated_data)
        question = serializer.validated_data["question"]
        if not can_submit(self.request.user, question):
            raise PermissionDenied("Please wait 30 seconds before submitting again.")
        submission = serializer.save(
            student=self.request.user,
            language_id=question.language_id,
            status=Submission.Status.PENDING,
        )
        evaluate_submission_task.delay(submission.pk)


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Question.objects.filter(is_active=True).select_related("module")


class ProgressViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        rows = student_progress(request.user)
        return Response(ProgressSerializer(rows, many=True).data)

    @action(detail=False, methods=["get"])
    def overall(self, request):
        eligible, pct = certificate_eligible(request.user)
        return Response({"percentage": pct, "certificate_eligible": eligible})


class SubmissionLatestViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"])
    def latest(self, request):
        question_id = request.query_params.get("question_id")
        if not question_id:
            return Response({"submission": None}, status=400)

        qs = Submission.objects.select_related("question").filter(student=request.user, question_id=question_id)
        submission = qs.order_by("-id").first()
        if not submission:
            return Response({"submission": None}, status=200)

        data = SubmissionSerializer(submission).data
        # DRF serializer uses numeric statuses for `status`; frontend expects string.
        # We send both for safety.
        return Response({"submission": {**data, "status": submission.status, "status_display": submission.get_status_display()}})
