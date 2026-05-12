import logging

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.problems.models import Problem
from apps.problems.services import ProblemService
from apps.test_cases.models import TestCase
from apps.test_cases.services import TestCaseService

logger = logging.getLogger(__name__)

DEMO_USERNAME = 'demo'

PROBLEMS = [
    {
        'title': 'Hello World',
        'description': 'Print the string `Hello, World!`.',
        'difficulty': 'easy',
        'category': 'basics',
        'test_cases': [
            {'input_data': 'run', 'expected_output': 'Hello, World!'},
            {'input_data': 'noop', 'expected_output': 'Hello, World!'},
        ],
    },
    {
        'title': 'FizzBuzz',
        'description': 'Print numbers 1..15 with Fizz/Buzz/FizzBuzz rules.',
        'difficulty': 'easy',
        'category': 'loops',
        'test_cases': [
            {
                'input_data': '15',
                'expected_output': (
                    '1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n'
                    '11\nFizz\n13\n14\nFizzBuzz'
                ),
            },
            {'input_data': '3', 'expected_output': '1\n2\nFizz'},
        ],
    },
    {
        'title': 'Two Sum',
        'description': 'Return indices of the two numbers that sum to target.',
        'difficulty': 'medium',
        'category': 'arrays',
        'test_cases': [
            {'input_data': '[2,7,11,15] 9', 'expected_output': '[0, 1]'},
            {'input_data': '[3,2,4] 6', 'expected_output': '[1, 2]'},
        ],
    },
]


class Command(BaseCommand):
    help = 'Seed demo data (idempotent). Use --reset to wipe seed rows first.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete seed-owned rows before seeding.',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options['reset']:
            self._reset()

        user = self._ensure_demo_user()
        problems_created, test_cases_created = self._ensure_problems()

        logger.info(
            'seed complete user=%s problems_created=%d test_cases_created=%d',
            user.username,
            problems_created,
            test_cases_created,
        )

    def _reset(self) -> None:
        titles = [p['title'] for p in PROBLEMS]
        deleted_tc, _ = TestCase.objects.filter(
            problem__title__in=titles
        ).delete()
        deleted_p, _ = Problem.objects.filter(title__in=titles).delete()
        logger.info(
            'seed reset removed problems=%d test_cases=%d',
            deleted_p,
            deleted_tc,
        )

    def _ensure_demo_user(self):
        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(
            username=DEMO_USERNAME,
        )
        if created:
            user.set_unusable_password()
            user.save()
            logger.info('seed user created username=%s', DEMO_USERNAME)
        else:
            logger.info('seed user exists username=%s', DEMO_USERNAME)
        return user

    def _ensure_problems(self) -> tuple[int, int]:
        problems_created = 0
        test_cases_created = 0

        for fixture in PROBLEMS:
            problem = Problem.objects.filter(title=fixture['title']).first()
            if problem is None:
                problem = ProblemService.create_problem(
                    title=fixture['title'],
                    description=fixture['description'],
                    difficulty=fixture['difficulty'],
                    category=fixture['category'],
                )
                problems_created += 1
            else:
                logger.info(
                    'seed problem exists id=%s title=%s',
                    problem.id,
                    problem.title,
                )

            for tc_fixture in fixture['test_cases']:
                exists = TestCase.objects.filter(
                    problem=problem,
                    input_data=tc_fixture['input_data'],
                ).exists()
                if exists:
                    logger.info(
                        'seed test_case exists problem_id=%s input=%r',
                        problem.id,
                        tc_fixture['input_data'],
                    )
                    continue

                TestCaseService.create_test_case(
                    problem_id=problem.id,
                    input_data=tc_fixture['input_data'],
                    expected_output=tc_fixture['expected_output'],
                )
                test_cases_created += 1

        return problems_created, test_cases_created
