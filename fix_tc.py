import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from core.models import Question, TestCase

testcases_data = {
    "Hello World": {
        "sample_input": "", "sample_output": "Hello, World!",
        "cases": [("", "Hello, World!")]
    },
    "Sum of Two Numbers": {
        "sample_input": "5 7", "sample_output": "12",
        "cases": [("5 7", "12"), ("-3 10", "7"), ("0 0", "0")]
    },
    "Area of Circle": {
        "sample_input": "5", "sample_output": "78.5",
        "cases": [("5", "78.5"), ("10", "314.0")]
    },
    "Temperature Conversion": {
        "sample_input": "0", "sample_output": "32",
        "cases": [("0", "32"), ("100", "212"), ("-40", "-40")]
    },
    "Simple Interest": {
        "sample_input": "1000 5 2", "sample_output": "100",
        "cases": [("1000 5 2", "100"), ("5000 7.5 3", "1125")]
    },
    "Even or Odd": {
        "sample_input": "4", "sample_output": "Even",
        "cases": [("4", "Even"), ("7", "Odd"), ("0", "Even")]
    },
    "Find Maximum": {
        "sample_input": "10 20", "sample_output": "20",
        "cases": [("10 20", "20"), ("50 -5", "50"), ("7 7", "7")]
    },
    "ASCII Value": {
        "sample_input": "A", "sample_output": "65",
        "cases": [("A", "65"), ("a", "97"), ("0", "48")]
    },
    "Swap Two Numbers": {
        "sample_input": "5 10", "sample_output": "10 5",
        "cases": [("5 10", "10 5"), ("-2 8", "8 -2")]
    },
    "Vowel or Consonant": {
        "sample_input": "A", "sample_output": "Vowel",
        "cases": [("A", "Vowel"), ("b", "Consonant"), ("E", "Vowel"), ("z", "Consonant")]
    }
}

for title, data in testcases_data.items():
    qs = Question.objects.filter(title=title, module__category='placement_training')
    for q in qs:
        q.sample_input = data["sample_input"]
        q.sample_output = data["sample_output"]
        q.save()
        
        q.test_cases.all().delete()
        
        for idx, (stdin, expected) in enumerate(data["cases"]):
            TestCase.objects.create(
                question=q,
                stdin=stdin,
                expected_output=expected,
                is_sample=(idx == 0)
            )
            
print("Fixed test cases for Module 1!")
