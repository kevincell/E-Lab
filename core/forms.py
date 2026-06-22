from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Module, Question, Submission, TestCase, User


class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "usn", "department", "semester")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.STUDENT
        if commit:
            user.save()
        return user


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ("code",)
        widgets = {
            "code": forms.Textarea(attrs={"rows": 18, "spellcheck": "false", "class": "code-editor"}),
        }


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ("name", "description", "level", "order", "is_active")


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = (
            "module",
            "title",
            "slug",
            "description",
            "difficulty",
            "sample_input",
            "sample_output",
            "starter_code",
            "language_id",
            "time_limit",
            "memory_limit_kb",
            "is_mandatory",
            "is_active",
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 8}),
            "starter_code": forms.Textarea(attrs={"rows": 8, "class": "code-editor"}),
            "sample_input": forms.Textarea(attrs={"rows": 4}),
            "sample_output": forms.Textarea(attrs={"rows": 4}),
        }


class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ("question", "stdin", "expected_output", "is_sample", "order")
        widgets = {
            "stdin": forms.Textarea(attrs={"rows": 4}),
            "expected_output": forms.Textarea(attrs={"rows": 4}),
        }
