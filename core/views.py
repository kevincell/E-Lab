from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .forms import ModuleForm, QuestionForm, StudentSignUpForm, SubmissionForm, TestCaseForm
from .models import Certificate, Module, Question, Submission, TestCase, User
from .serializers import ProgressSerializer, QuestionSerializer, SubmissionSerializer
from .services import certificate_eligible, generate_certificate, overall_percentage, student_progress
from .tasks import evaluate_submission_task


class AppLoginView(LoginView):
    template_name = "registration/login.html"


class AppLogoutView(LogoutView):
    pass


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

    if request.user.is_faculty_like:
        modules = Module.objects.annotate(question_count=Count("questions"))
        recent = Submission.objects.select_related("student", "question")[:12]
        students = User.objects.filter(role=User.Role.STUDENT).count()
        return render(
            request,
            "faculty/dashboard.html",
            {
                "modules": modules,
                "recent_submissions": recent,
                "students": students,
                "questions": Question.objects.count(),
            },
        )

    progress_rows = student_progress(request.user)
    modules = Module.objects.filter(is_active=True).prefetch_related("questions")
    pct = overall_percentage(request.user)
    eligible, _ = certificate_eligible(request.user)
    certificates = request.user.certificates.all()
    return render(
        request,
        "student/dashboard.html",
        {
            "modules": modules,
            "progress_rows": progress_rows,
            "overall_percentage": pct,
            "certificate_eligible": eligible,
            "certificates": certificates,
        },
    )


@login_required
def module_detail(request, module_id):
    module = get_object_or_404(Module, pk=module_id, is_active=True)
    questions = module.questions.filter(is_active=True)
    accepted_ids = set(
        Submission.objects.filter(
            student=request.user,
            status=Submission.Status.ACCEPTED,
            question__in=questions,
        ).values_list("question_id", flat=True)
    )
    return render(
        request,
        "student/module_detail.html",
        {"module": module, "questions": questions, "accepted_ids": accepted_ids},
    )


@login_required
def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id, is_active=True)
    latest = Submission.objects.filter(student=request.user, question=question).first()
    initial = {"code": latest.code if latest else question.starter_code}
    form = SubmissionForm(request.POST or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        submission = form.save(commit=False)
        submission.student = request.user
        submission.question = question
        submission.language_id = question.language_id
        submission.save()
        evaluate_submission_task.delay(submission.pk)
        messages.success(request, "Submission queued. Refresh in a moment for the result.")
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
def faculty_module_form(request, module_id=None):
    faculty_required(request.user)
    module = get_object_or_404(Module, pk=module_id) if module_id else None
    form = ModuleForm(request.POST or None, instance=module)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Module saved.")
        return redirect("dashboard")
    return render(request, "faculty/form.html", {"form": form, "title": "Module"})


@login_required
def faculty_question_form(request, question_id=None):
    faculty_required(request.user)
    question = get_object_or_404(Question, pk=question_id) if question_id else None
    form = QuestionForm(request.POST or None, instance=question)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        if not obj.created_by_id:
            obj.created_by = request.user
        obj.save()
        messages.success(request, "Question saved. Add hidden tests before students use it.")
        return redirect("faculty_question_edit", obj.pk)
    tests = question.test_cases.all() if question else []
    return render(request, "faculty/question_form.html", {"form": form, "question": question, "tests": tests})


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


class SubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Submission.objects.select_related("question", "student")
        if self.request.user.is_faculty_like:
            return qs
        return qs.filter(student=self.request.user)

    def perform_create(self, serializer):
        question = serializer.validated_data["question"]
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
