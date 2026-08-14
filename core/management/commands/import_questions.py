from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Import questions from CSV files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--second-year',
            action='store_true',
            help='Import second year questions instead of first year'
        )

    def handle(self, *args, **options):
        if options['second_year']:
            self.stdout.write(self.style.SUCCESS('Importing second year questions...'))
            # Call the second year import script
            from scripts.import_second_year import import_second_year_questions
            import_second_year_questions()
        else:
            self.stdout.write(self.style.SUCCESS('Importing first year questions...'))
            # Call the existing import script
            script_path = os.path.join(os.path.dirname(__file__), '../../../scripts/verify_and_import.py')
            if os.path.exists(script_path):
                with open(script_path, 'r') as f:
                    exec(f.read())
            else:
                self.stdout.write(self.style.ERROR('First year questions import script not found'))
        
        self.stdout.write(self.style.SUCCESS('Questions import completed'))