from django.core.management.base import BaseCommand
from django.utils.text import slugify
import requests
from core.models import Question, TestCase, Module, User

class Command(BaseCommand):
    help = "Import LeetCode questions into E-Lab"

    def add_arguments(self, parser):
        parser.add_argument('--question', type=str, help="LeetCode question slug or ID to import")
        parser.add_argument('--module', type=str, help="Module name to assign the question to")
        parser.add_argument('--difficulty', type=str, choices=['easy', 'medium', 'hard'], default='easy', help="Question difficulty")
        parser.add_argument('--csv-level', type=int, default=1, help="CSV level for the question")

    def handle(self, *args, **options):
        # First, let's get or create a faculty user
        faculty, _ = User.objects.get_or_create(username='faculty', defaults={'email': 'faculty@elab.local', 'first_name': 'Faculty', 'role': User.Role.FACULTY})
        
        # Get or create module
        module_name = options['module'] or 'LeetCode'
        module, _ = Module.objects.get_or_create(name=module_name, defaults={'level': 1, 'order': 1, 'description': 'LeetCode questions'})
        
        if options['question']:
            self.import_single_question(options['question'], module, options['difficulty'], options['csv_level'], faculty)
        else:
            self.stdout.write(self.style.WARNING('Please specify --question <slug or ID>'))

    def import_single_question(self, question_id_or_slug, module, difficulty, csv_level, faculty):
        self.stdout.write(f'Fetching LeetCode question: {question_id_or_slug}')
        
        # LeetCode GraphQL API endpoint
        url = 'https://leetcode.com/graphql'
        headers = {
            'Content-Type': 'application/json',
            'Referer': 'https://leetcode.com',
        }
        
        # GraphQL query to get question details
        query = '''
        query getQuestionDetail($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionId
                title
                titleSlug
                difficulty
                content
                sampleInput
                sampleOutput
                codeSnippets {
                    langSlug
                    code
                }
            }
        }
        '''
        
        # If input is a number (question ID), we need to get the slug first
        slug = question_id_or_slug
        if question_id_or_slug.isdigit():
            # Need another query to get the slug from ID
            list_query = '''
            query getQuestionList {
                allQuestions {
                    id
                    questionId
                    titleSlug
                }
            }
            '''
            try:
                response = requests.post(url, json={'query': list_query}, headers=headers, timeout=10)
                response.raise_for_status()
                data = response.json()
                all_questions = data.get('data', {}).get('allQuestions', [])
                found = next((q for q in all_questions if q.get('questionId') == question_id_or_slug), None)
                if not found:
                    self.stdout.write(self.style.ERROR(f'Could not find question with ID: {question_id_or_slug}'))
                    return
                slug = found.get('titleSlug')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error fetching question list: {str(e)}'))
                return
        
        try:
            variables = {'titleSlug': slug}
            response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            question_data = data.get('data', {}).get('question')
            
            if not question_data:
                self.stdout.write(self.style.ERROR(f'Could not find question: {slug}'))
                return
            
            self.stdout.write(self.style.SUCCESS(f'Found question: {question_data["title"]}'))
            
            # Get C starter code
            c_starter = ''
            for snippet in question_data.get('codeSnippets', []):
                if snippet.get('langSlug') == 'c':
                    c_starter = snippet.get('code')
                    break
            
            # Create question
            question, created = Question.objects.get_or_create(
                module=module,
                slug=slugify(question_data['title']),
                defaults={
                    'title': question_data['title'],
                    'description': question_data.get('content', ''),
                    'difficulty': difficulty,
                    'csv_level': csv_level,
                    'sample_input': question_data.get('sampleInput', ''),
                    'sample_output': question_data.get('sampleOutput', ''),
                    'starter_code': c_starter,
                    'created_by': faculty,
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created new question: {question.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Question already exists: {question.title}'))
            
            # Create sample test case
            if question_data.get('sampleInput') or question_data.get('sampleOutput'):
                TestCase.objects.get_or_create(
                    question=question,
                    order=1,
                    is_sample=True,
                    defaults={'stdin': question_data.get('sampleInput', ''), 'expected_output': question_data.get('sampleOutput', '')}
                )
                self.stdout.write(self.style.SUCCESS('Added sample test case'))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing question: {str(e)}'))
