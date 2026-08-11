from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from core.models import User


class Command(BaseCommand):
    help = "Create demo users and link them to any seeded courses."

    def handle(self, *args, **options):
        user_model = get_user_model()
        admin = user_model.objects.filter(username="admin").first()
        if not admin:
            admin = user_model.objects.create_superuser(
                username="admin",
                email="admin@elab.local",
                password="admin12345",
                role=User.Role.ADMIN,
            )

        faculty, created = user_model.objects.get_or_create(
            username="faculty",
            defaults={
                "email": "faculty@elab.local",
                "first_name": "Faculty",
                "role": User.Role.FACULTY,
                "is_staff": True,
            },
        )
        if created:
            faculty.set_password("faculty12345")
            faculty.save()

        student, created = user_model.objects.get_or_create(
            username="student",
            defaults={
                "email": "student@elab.local",
                "first_name": "Demo",
                "last_name": "Student",
                "usn": "4NM00CS001",
                "department": "CSE",
                "semester": 1,
                "role": User.Role.STUDENT,
            },
        )
        if created:
            student.set_password("student12345")
            student.save()

        # Assign faculty demo user to all existing active courses
        # (Courses are created automatically when verify_and_import.py is run)
        from core.models import Course
        for course in Course.objects.filter(is_active=True):
            faculty.managed_courses.add(course)

        self.stdout.write(self.style.SUCCESS("Demo data ready."))

