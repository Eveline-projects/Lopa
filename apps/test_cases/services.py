from .models import TestCase
from apps.problems.models import Problem
from django.core.exceptions import ValidationError


class TestCaseService:
    def create_test_case(
            self,
            problem: Problem,
            input_data: str,
            expected_output: str,
            is_hidden: bool = False
    ) -> TestCase:
        if not input_data.strip():
            raise ValidationError('Input data cannot be empty')
        if not expected_output.strip():
            raise ValidationError('Expected output cannot be empty')

        return TestCase.objects.create(
            problem=problem,
            input_data=input_data,
            expected_output=expected_output,
            is_hidden=is_hidden,
        )
