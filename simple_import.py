#!/usr/bin/env python
import os
import sys
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from core.models import User, Question, Module
from core.views import import_question_csv

def simple_import():
    """Simple question import that doesn't require Docker socket access."""
    print("Starting simple import...")
    
    # Get or create faculty user
    faculty, _ = User.objects.get_or_create(
        username="faculty_admin",
        defaults={
            "is_staff": True,
            "role": User.Role.FACULTY,
            "email": "faculty@example.com"
        }
    )
    
    # Path to CSV files
    csv_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "generated_level_question_csvs")
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
    
    print(f"Looking for CSV files in: {csv_dir}")
    
    # Check if directory exists
    if not os.path.exists(csv_dir):
        print(f"ERROR: CSV directory not found at {csv_dir}")
        print("Please ensure the 'generated_level_question_csvs' directory exists")
        return
    
    # Import each CSV file
    for filename in csv_files:
        filepath = os.path.join(csv_dir, filename)
        if not os.path.exists(filepath):
            print(f"WARNING: File not found: {filepath}")
            continue
            
        print(f"Importing {filename}...")
        try:
            with open(filepath, "rb") as f:
                result = import_question_csv(f, faculty)
                print(f"Successfully imported {filename}: {result['created']} created, {result['updated']} updated")
        except Exception as e:
            print(f"ERROR importing {filename}: {str(e)}")
    
    print("Import completed!")

if __name__ == "__main__":
    simple_import()