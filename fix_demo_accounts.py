import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from core.models import User

print("Fixing demo accounts and passwords...")

# 1. Create HOD
hod, created = User.objects.get_or_create(
    username="hod",
    defaults={
        "email": "hod@example.com",
        "first_name": "Head",
        "last_name": "of Department",
        "role": User.Role.HOD,
    }
)
hod.set_password("hodpassword")
hod.save()
print(f"HOD account 'hod' password set to 'hodpassword'.")

# 2. Fix Faculty
faculty_data = [
    {"username": "faculty_cs", "password": "faculty123"},
    {"username": "faculty_it", "password": "faculty123"},
]

for fd in faculty_data:
    try:
        user = User.objects.get(username=fd["username"])
        user.set_password(fd["password"])
        user.save()
        print(f"Faculty '{user.username}' password reset to '{fd['password']}'.")
    except User.DoesNotExist:
        print(f"Faculty '{fd['username']}' does not exist! Please run seed_demo_fixed script first.")

# 3. Fix Students
student_data = [
    {"username": "student_fy_01", "password": "student123"},
    {"username": "student_fy_02", "password": "student123"},
    {"username": "student_fy_03", "password": "student123"},
    {"username": "student_sy_01", "password": "student123"},
    {"username": "student_sy_02", "password": "student123"},
    {"username": "student_sy_03", "password": "student123"},
]

for sd in student_data:
    try:
        user = User.objects.get(username=sd["username"])
        user.set_password(sd["password"])
        user.save()
        print(f"Student '{user.username}' password reset to '{sd['password']}'.")
    except User.DoesNotExist:
        print(f"Student '{sd['username']}' does not exist! Please run seed_demo_fixed script first.")

print("Finished fixing demo accounts!")
