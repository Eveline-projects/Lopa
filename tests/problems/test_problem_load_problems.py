import json
import os
from io import StringIO
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.core.management import CommandError, call_command
from django.test import TestCase

from apps.problems.models import Problem
from apps.problems.services import ProblemService


class LoadProblemsCommandTest(TestCase):
    def setUp(self):
        self.test_file = 'test_problems.json'
        self.valid_data = [
            {
                'title': 'Two Sum',
                'description': 'Target sum indices',
                'difficulty': 'easy',
                'category': 'Arrays',
                'is_active': True,
            }
        ]
        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump(self.valid_data, f)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_load_problems_creates_new_record(self):
        out = StringIO()
        err = StringIO()

        call_command('load_problems', self.test_file, stdout=out, stderr=err)

        self.assertEqual(err.getvalue(), '')
        self.assertIn('Created new problem: Two Sum', out.getvalue())
        self.assertEqual(Problem.objects.count(), 1)

        problem = Problem.objects.get(title='Two Sum')
        self.assertEqual(problem.difficulty, 'easy')
        self.assertTrue(problem.is_active)

    def test_load_problems_updates_existing_record(self):
        ProblemService.create_problem(
            title='Two Sum',
            description='Old',
            difficulty='hard',
            category='Arrays',
        )

        out = StringIO()
        err = StringIO()

        call_command('load_problems', self.test_file, stdout=out, stderr=err)

        self.assertEqual(err.getvalue(), '')
        self.assertIn('Updated existing problem: Two Sum', out.getvalue())
        self.assertEqual(Problem.objects.count(), 1)

        updated = Problem.objects.get(title='Two Sum')
        self.assertEqual(updated.description, 'Target sum indices')
        self.assertEqual(updated.difficulty, 'easy')
        self.assertEqual(updated.category, 'Arrays')

    def test_load_problems_fails_on_invalid_json(self):
        bad_file = 'bad.json'
        with open(bad_file, 'w', encoding='utf-8') as f:
            f.write("{'broken': json}")

        try:
            with self.assertRaises(CommandError) as cm:
                call_command('load_problems', bad_file)

            self.assertIn('Invalid JSON', str(cm.exception))
        finally:
            if os.path.exists(bad_file):
                os.remove(bad_file)

    def test_load_problems_fails_on_missing_file(self):
        with self.assertRaises(CommandError) as cm:
            call_command('load_problems', 'non_existent.json')

        self.assertIn('File not found', str(cm.exception))

    def test_load_problems_fails_when_required_key_is_missing(self):
        invalid_data = [
            {
                'title': 'Two Sum',
                'description': 'Target sum indices',
                'difficulty': 'easy',
                # missing "category"
            }
        ]

        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump(invalid_data, f)

        with self.assertRaises(CommandError) as cm:
            call_command('load_problems', self.test_file)

        self.assertIn(
            'Missing required keys in JSON item: category', str(cm.exception)
        )
        self.assertEqual(Problem.objects.count(), 0)

    @patch(
        'apps.problems.management.commands.load_problems.ProblemService.upsert_problem'
    )
    def test_load_problems_writes_validation_error_to_stderr_and_continues(
        self, mock_upsert
    ):
        mock_upsert.side_effect = [
            ValidationError('Invalid difficulty'),
            (
                Problem(
                    title='Valid problem',
                    description='Some description',
                    difficulty='easy',
                    category='Arrays',
                    is_active=True,
                ),
                True,
            ),
        ]

        mixed_data = [
            {
                'title': 'Broken problem',
                'description': 'Bad description',
                'difficulty': 'wrong',
                'category': 'Arrays',
            },
            {
                'title': 'Valid problem',
                'description': 'Some description',
                'difficulty': 'easy',
                'category': 'Arrays',
            },
        ]

        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump(mixed_data, f)

        out = StringIO()
        err = StringIO()

        call_command('load_problems', self.test_file, stdout=out, stderr=err)

        self.assertIn('Invalid record:', err.getvalue())
        self.assertIn('Invalid difficulty', err.getvalue())
        self.assertIn('Created new problem: Valid problem', out.getvalue())
        self.assertEqual(mock_upsert.call_count, 2)

    def test_load_problems_is_idempotent_and_does_not_duplicate_test_cases(
        self,
    ):
        data_with_tests = [
            {
                'title': 'Idempotent Problem',
                'description': 'Testing duplicates',
                'difficulty': 'easy',
                'category': 'Arrays',
                'is_active': True,
                'test_cases': [
                    {'input_data': '1', 'expected_output': '1'},
                    {'input_data': '2', 'expected_output': '2'},
                ],
            }
        ]

        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump(data_with_tests, f)

        call_command('load_problems', self.test_file)
        problem = Problem.objects.get(title='Idempotent Problem')

        self.assertEqual(problem.test_cases.count(), 2)

        call_command('load_problems', self.test_file)

        self.assertEqual(problem.test_cases.count(), 2)
