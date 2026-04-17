import uuid
from django.db.models import QuerySet
from .models import TestCase
from apps.problems.models import Problem
from django.core.exceptions import ValidationError

from .repositories import TestCaseRepository


class TestCaseService:
    @staticmethod
    def create_test_case(
            problem: Problem,
            input_data: str,
            expected_output: str,
            is_hidden: bool = False
    ) -> TestCase:
        if not input_data or not input_data.strip():
            raise ValidationError('Input data cannot be empty')

        if not expected_output or not expected_output.strip():
            raise ValidationError('Expected output cannot be empty')

        return TestCase.objects.create(
            problem=problem,
            input_data=input_data,
            expected_output=expected_output,
            is_hidden=is_hidden,
        )

    @staticmethod
    def get_test_cases_for_problem(problem_id: uuid.UUID) -> QuerySet[TestCase]:
        return TestCaseRepository.get_test_cases_for_problem(problem_id)

    @staticmethod
    def get_test_case_by_id(test_case_id: uuid.UUID) -> TestCase:
        return TestCaseRepository.get_by_id(test_case_id)
