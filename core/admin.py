from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Certificate, Module, Progress, Question, Submission, TestCase, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("e-Lab profile", {"fields": ("usn", "role", "department", "semester")}),
    )
    list_display = ("username", "email", "usn", "role", "department", "semester", "is_staff")
    list_filter = ("role", "department", "semester", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name", "usn")


class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 1


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("title", "module", "difficulty", "language_id", "is_mandatory", "is_active")
    list_filter = ("module", "difficulty", "is_mandatory", "is_active")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [TestCaseInline]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("student", "question", "status", "score", "submitted_at", "judged_at")
    list_filter = ("status", "question__module")
    search_fields = ("student__username", "student__usn", "question__title")


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ("student", "module", "attempted", "completed", "percentage", "updated_at")
    list_filter = ("module",)


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("student", "semester", "completion_percentage", "issued_at")
    search_fields = ("student__username", "student__usn", "verification_hash")
