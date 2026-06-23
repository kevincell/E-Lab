from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="submission",
            name="manually_graded",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="submission",
            name="plagiarism_flagged",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="submission",
            name="plagiarism_notes",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="submission",
            name="graded_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="graded_submissions",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="LabSession",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField(default=django.utils.timezone.localdate)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "module",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lab_sessions",
                        to="core.module",
                    ),
                ),
                (
                    "students_present",
                    models.ManyToManyField(
                        blank=True,
                        related_name="lab_sessions_present",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-date", "module__order"],
                "unique_together": {("date", "module")},
            },
        ),
        migrations.CreateModel(
            name="Attendance",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("login_time", models.DateTimeField(auto_now_add=True)),
                ("logout_time", models.DateTimeField(blank=True, null=True)),
                ("time_spent_minutes", models.PositiveIntegerField(default=0)),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attendance_rows",
                        to="core.labsession",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attendance_rows",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-login_time"],
                "unique_together": {("student", "session", "login_time")},
            },
        ),
    ]
