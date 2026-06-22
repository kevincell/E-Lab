from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from core.models import Module, Question, TestCase, User


class Command(BaseCommand):
    help = "Create starter modules, questions, test cases, and demo users."

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

        basics, _ = Module.objects.get_or_create(
            name="Basics and I/O",
            defaults={
                "description": "Introductory C programs using input, output, variables, and operators.",
                "level": 1,
                "order": 1,
            },
        )
        control, _ = Module.objects.get_or_create(
            name="Control Flow",
            defaults={
                "description": "Branching and loops.",
                "level": 2,
                "order": 2,
            },
        )

        self.create_question(
            basics,
            "Print Hello",
            "Write a C program that prints Hello.",
            "",
            "Hello",
            '#include <stdio.h>\nint main() {\n    printf("Hello");\n    return 0;\n}\n',
            faculty,
        )
        self.create_question(
            basics,
            "Sum Two Numbers",
            "Read two integers and print their sum.",
            "2 5",
            "7",
            "#include <stdio.h>\nint main() {\n    int a, b;\n    scanf(\"%d %d\", &a, &b);\n    printf(\"%d\", a + b);\n    return 0;\n}\n",
            faculty,
            hidden=[("10 20", "30"), ("-5 8", "3")],
        )
        self.create_question(
            control,
            "Even or Odd",
            "Read an integer and print Even if it is even, otherwise print Odd.",
            "4",
            "Even",
            "#include <stdio.h>\nint main() {\n    int n;\n    scanf(\"%d\", &n);\n    if (n % 2 == 0) printf(\"Even\"); else printf(\"Odd\");\n    return 0;\n}\n",
            faculty,
            hidden=[("7", "Odd"), ("100", "Even")],
        )

        self.stdout.write(self.style.SUCCESS("Demo data ready."))

    def create_question(self, module, title, description, sample_in, sample_out, starter, faculty, hidden=None):
        question, _ = Question.objects.get_or_create(
            module=module,
            slug=slugify(title),
            defaults={
                "title": title,
                "description": description,
                "sample_input": sample_in,
                "sample_output": sample_out,
                "starter_code": starter,
                "created_by": faculty,
            },
        )
        TestCase.objects.get_or_create(
            question=question,
            order=1,
            is_sample=True,
            defaults={"stdin": sample_in, "expected_output": sample_out},
        )
        for idx, (stdin, expected) in enumerate(hidden or [(sample_in, sample_out)], start=2):
            TestCase.objects.get_or_create(
                question=question,
                order=idx,
                is_sample=False,
                defaults={"stdin": stdin, "expected_output": expected},
            )
