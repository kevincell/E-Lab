import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.template.loader import get_template

try:
    template = get_template('student/question_detail.html')
    print("Template parsed successfully!")
except Exception as e:
    import traceback
    traceback.print_exc()
