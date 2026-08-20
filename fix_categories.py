import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from core.models import Module

# Modules 1-10 are C Programming (1st Year)
updated_c = Module.objects.filter(order__lte=10).update(category="c_programming")
print(f"Updated {updated_c} modules to c_programming")

# Modules 11-15 are Placement Training (2nd Year)
updated_pt = Module.objects.filter(order__gt=10, order__lte=15).update(category="placement_training")
print(f"Updated {updated_pt} modules to placement_training")

# Modules 16+ are Advanced Placement Training (3rd Year)
updated_apt = Module.objects.filter(order__gt=15).update(category="advanced_placement_training")
print(f"Updated {updated_apt} modules to advanced_placement_training")

print("Successfully categorized all existing modules!")
