import os
import sys
import django


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# FIX: Use dynamic path instead of hardcoded Windows path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.insert(0, project_root)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
os.environ["USE_SQLITE"] = "true"
django.setup()

from core.models import User, Module, Question
from core.views import import_question_csv
from core.services import choose_adaptive_questions

# Get or create faculty user for import
faculty, _ = User.objects.get_or_create(username="admin_gen", defaults={"is_staff": True, "role": User.Role.FACULTY, "email": "admin@example.com"})

# Get or create dummy student for testing
student, _ = User.objects.get_or_create(username="student_test", defaults={"role": User.Role.STUDENT, "email": "student@example.com", "usn": "1RN21CS999"})

csv_files = [
    "Module1_Basics_IO_Levels.csv",
    "Module2_Operators_Expressions_Levels.csv",
    "Module3_Conditionals_Loops_Levels.csv",
    "Module4_Arrays_Levels.csv",
    "Module5_Strings_Levels.csv",
    "Module6_Functions_Levels.csv",
    "Module7_Pointers_Levels.csv",
    "Module8_Structures_Levels.csv",
    "Module9_File_Handling_Levels.csv",
    "Module10_Advanced_Concepts_Levels.csv"
]

print("Starting CSV import...")
imported_modules = []
for filename in csv_files:
    filepath = os.path.join(PROJECT_ROOT, "generated_level_question_csvs", filename)
    with open(filepath, "rb") as f:
        res = import_question_csv(f, faculty)
    
    module = res["module"]
    imported_modules.append(module)
    total = module.questions.count()
    mand = module.questions.filter(is_mandatory=True).count()
    print(f"[{module.name} (Order {module.order})] Created: {res['created']} | Updated: {res['updated']} | Total Qs: {total} | Mandatory Qs: {mand}")

print("\nTesting Adaptive Selection & Mandatory Guarantee...")
for module in imported_modules:  # test all modules
    # Test Easy randomization
    easy_1 = choose_adaptive_questions(student, module, Question.Difficulty.EASY, count=5)
    easy_2 = choose_adaptive_questions(student, module, Question.Difficulty.EASY, count=5)
    e_ids_1 = sorted([q.slug for q in easy_1])
    e_ids_2 = sorted([q.slug for q in easy_2])
    print(f"\n{module.name} - Easy Pick 1 count: {len(e_ids_1)}")
    print(f"{module.name} - Easy Pick 2 count: {len(e_ids_2)}")
    
    # Test Hard Mandatory Guarantee
    hard_qs = choose_adaptive_questions(student, module, Question.Difficulty.HARD, count=5)
    hard_slugs = [q.slug for q in hard_qs]
    mand_slugs = [q.slug for q in module.questions.filter(difficulty=Question.Difficulty.HARD, is_mandatory=True)]
    
    all_mand_included = all(s in hard_slugs for s in mand_slugs)
    print(f"{module.name} - Hard Pick count: {len(hard_slugs)} | Mandatory count required: {len(mand_slugs)} | All Mandatory Included: {all_mand_included}")

print("\nVerification Complete!")
