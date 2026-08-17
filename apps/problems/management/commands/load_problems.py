import json
import logging

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.problems.services import ProblemService
from apps.test_cases.services import TestCaseService

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Loads initial algorithm problems from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path', type=str, help='Path to the JSON file'
        )

    def handle(self, *args, **options):
        file_path = options['file_path']

        logger.info('Starting problem seeding from file=%s', file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError as e:
                    logger.error(
                        'JSON decoding failed file=%s error=%s',
                        file_path,
                        str(e),
                    )
                    raise CommandError(f'Invalid JSON: {e}')
        except FileNotFoundError:
            logger.error('File not found path=%s', file_path)
            raise CommandError(f'File not found: {file_path}')

        created_count = 0
        updated_count = 0

        try:
            with transaction.atomic():
                for item in data:
                    required_keys = {
                        'title',
                        'description',
                        'difficulty',
                        'category',
                    }
                    missing = required_keys - item.keys()
                    if missing:
                        missing_keys = ', '.join(sorted(missing))
                        logger.error(
                            'Validation failed: missing keys=%s in item',
                            missing_keys,
                        )
                        raise CommandError(
                            f'Missing required keys in JSON item: {missing_keys}'
                        )
                    try:
                        problem, created = ProblemService.upsert_problem(
                            title=item['title'],
                            description=item['description'],
                            difficulty=item['difficulty'],
                            category=item['category'],
                            is_active=item.get('is_active', True),
                        )

                        if 'test_cases' in item:
                            problem.test_cases.all().delete()

                            for tc in item['test_cases']:
                                TestCaseService.create_test_case(
                                    problem_id=problem.id,
                                    input_data=tc['input_data'],
                                    expected_output=tc['expected_output'],
                                )

                        if created:
                            created_count += 1
                            action_performed = 'Created new problem'
                        else:
                            updated_count += 1
                            action_performed = 'Updated existing problem'

                        logger.debug(
                            '%s: id=%s title=%s',
                            action_performed,
                            problem.id,
                            problem.title,
                        )

                        self.stdout.write(
                            self.style.SUCCESS(
                                f'{action_performed}: {problem.title}'
                            )
                        )
                    except ValidationError as validation_error:
                        logger.warning(
                            'Skipping invalid problem item_title=%s error=%s',
                            item.get('title'),
                            str(validation_error),
                        )
                        self.stderr.write(
                            self.style.ERROR(
                                f'Invalid record: {validation_error}'
                            )
                        )
            logger.info(
                'Problem seeding completed successfully, file=%s created=%d updated=%d',
                file_path,
                created_count,
                updated_count,
            )

        except Exception as unexpected_error:
            if isinstance(unexpected_error, CommandError):
                raise

            logger.exception('Unexpected error during problem seeding')
            raise CommandError(
                f'Unexpected error during seeding: {unexpected_error}'
            )
