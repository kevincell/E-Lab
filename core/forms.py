from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Module, Question, Submission, TestCase, User


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={"accept": ".csv", "multiple": True}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_clean(file, initial) for file in data]
        return [single_clean(data, initial)]


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


class CSVQuestionUploadForm(forms.Form):
    files = MultipleFileField(
        label="CSV files",
        help_text="Upload one or more module CSV files with Question_ID, Topic, Level, Difficulty, and score columns.",
    )


class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["module"].empty_label = "Choose a module"
        self.fields["title"].widget.attrs.update({"placeholder": "Longest substring without repeating characters"})
        self.fields["slug"].widget.attrs.update({"placeholder": "longest-substring"})
        self.fields["description"].widget.attrs.update(
            {
                "placeholder": (
                    "Describe the task, input format, output format, and constraints. "
                    "Students should read from stdin and print only the expected answer."
                )
            }
        )
        self.fields["sample_input"].widget.attrs.update({"placeholder": "abcabcbb"})
        self.fields["sample_output"].widget.attrs.update({"placeholder": "3"})
        self.fields["starter_code"].widget.attrs.update(
            {
                "placeholder": (
                    "#include <stdio.h>\n\n"
                    "int main(void) {\n"
                    "    /* Read from stdin and print exact output only. */\n"
                    "    return 0;\n"
                    "}\n"
                )
            }
        )
        self.fields["time_limit"].help_text = "Seconds allowed for each test case."
        self.fields["memory_limit_kb"].help_text = "Memory limit in KB. 128000 is usually enough for C basics."

    class Meta:
        model = Question
        fields = (
            "module",
            "title",
            "slug",
            "description",
            "difficulty",
            "csv_level",
            "level_range",
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


class QuickTestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ("stdin", "expected_output", "is_sample", "order")
        widgets = {
            "stdin": forms.Textarea(attrs={"rows": 4, "placeholder": "Input passed through stdin"}),
            "expected_output": forms.Textarea(attrs={"rows": 4, "placeholder": "Exact expected output"}),
            "order": forms.NumberInput(attrs={"min": 1}),
        }
