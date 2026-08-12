from django.core.management.base import BaseCommand
from core.models import User


class Command(BaseCommand):
    help = "Create a sample HoD account (username=hod, password=hod@elab2026)"

    def handle(self, *args, **options):
        if User.objects.filter(username="hod").exists():
            self.stdout.write(self.style.WARNING("HoD account already exists."))
            return

        user = User.objects.create_user(
            username="hod",
            password="hod@elab2026",
            role=User.Role.HOD,
            first_name="Head",
            last_name="of Department",
            department="Computer and Communication Engineering",
            is_staff=True,
        )
        self.stdout.write(self.style.SUCCESS(f"HoD account created: {user.username}"))
