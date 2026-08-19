import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from core.models import Course, Module, Question, TestCase, User
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Seeds Advanced Placement Training curriculum data from JSON'

    def handle(self, *args, **options):
        self.stdout.write("Seeding Advanced Technical Placement Training curriculum...")
        
        json_path = os.path.join(settings.BASE_DIR, "data", "advanced_placement_training_questions.json")
        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f"JSON file not found at {json_path}"))
            return

        with open(json_path, "r") as f:
            questions_data = json.load(f)

        # Clean up existing advanced placement training modules to start fresh
        Module.objects.filter(category="advanced_placement_training").delete()

        course, _ = Course.objects.get_or_create(
            slug="advanced-technical-placement-training",
            defaults={
                "name": "Advanced Technical Placement Training",
                "description": "Exclusive 14-week program for 5th semester CCE students.",
                "year": 3,
                "semester": 5,
                "is_active": True
            }
        )

        weeks = [
            (1, "Week 1: Complexity Analysis", "Revision of Programming Fundamentals, Complexity Analysis"),
            (2, "Week 2: Arrays and Strings", "Sliding Window, Prefix Sum, String manipulation problems"),
            (3, "Week 3: Recursion & Backtracking", "Sudoku, Maze, N-Queens, Divide & Conquer"),
            (4, "Week 4: Linked Lists & Stacks", "Reverse linked list, Stack using arrays, Queue implementation"),
            (5, "Week 5: Trees and BST", "Tree traversals, BST operations"),
            (6, "Week 6: Graphs and Heaps", "DFS/BFS Traversals, Priority Queues"),
            (7, "Week 7: Hashing and Searching", "Hash Maps, Frequency counting, Collision handling"),
            (8, "Week 8: Sorting, Greedy & DP", "Merge Sort, Quick Sort, DP basics, Knapsack"),
            (9, "Week 9: OOP & Design Patterns", "Classes, Objects, Inheritance, Polymorphism, LLD"),
            (10, "Week 10: OS Fundamentals", "Process vs Thread, CPU Scheduling, Synchronization, Deadlocks"),
        ]

        admin_user = User.objects.filter(is_superuser=True).first() or User.objects.first()

        for week_num, name, desc in weeks:
            module, _ = Module.objects.get_or_create(
                name=name,
                defaults={
                    "description": desc,
                    "order": week_num,
                    "level": week_num,
                    "category": "advanced_placement_training",
                    "course": course,
                    "is_active": True
                }
            )
            
            # Add Questions
            week_questions = questions_data.get(str(week_num), [])
            for q_data in week_questions:
                slug = slugify(q_data["title"]) + f"-adv-w{week_num}"
                question, created = Question.objects.get_or_create(
                    module=module,
                    slug=slug,
                    defaults={
                        "title": q_data["title"],
                        "description": q_data["desc"],
                        "difficulty": q_data["diff"],
                        "allow_multiple_languages": True,
                        "is_mandatory": True,
                        "is_active": True,
                        "created_by": admin_user,
                    }
                )
                
                if created:
                    for idx, tc in enumerate(q_data.get("test_cases", [])):
                        TestCase.objects.create(
                            question=question,
                            stdin=tc["in"],
                            expected_output=tc["out"],
                            is_sample=tc["is_sample"],
                            order=idx + 1
                        )
        
        self.stdout.write(self.style.SUCCESS("✅ Advanced Placement Training JSON seeding completed!"))
