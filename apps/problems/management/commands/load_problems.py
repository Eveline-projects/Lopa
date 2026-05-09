import json
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from apps.problems.services import ProblemService


class Command(BaseCommand):
    help = 'Loads initial algorithm problems from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path', type=str, help='Path to the JSON file'
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            for item in data:
                try:
                    if not all(
                        k in item
                        for k in (
                            'title',
                            'description',
                            'difficulty',
                            'category',
                        )
                    ):
                        self.stdout.write(
                            self.style.WARNING(
                                f'Skipping: Missiong fields in {item.get("title", "Unknown")}'
                            )
                        )
                        continue
                    problem, created = ProblemService.seed_problem(
                        title=item['title'],
                        description=item['description'],
                        difficulty=item['difficulty'],
                        category=item['category'],
                        is_active=item.get('is_active', True),
                    )

                    action_performed = (
                        'Created new problem'
                        if created
                        else 'Updated existing problem'
                    )

                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Successfully loaded: {action_performed}: {problem.title}'
                        )
                    )
                except ValidationError as validation_error:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Invalid record {item.get("title")}: {validation_error}'
                        )
                    )
                except Exception as unexpected_error:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Error loading {item.get("title")}: {str(unexpected_error)}'
                        )
                    )

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
