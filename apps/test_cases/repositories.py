import uuid
from .models import TestCase
from apps.problems.models import Problem


class TestCaseRepository:
    @staticmethod
    def save(test_case: TestCase) -> TestCase:
        test_case.full_clean()
        test_case.save()
        return test_case

    @staticmethod
    def create(
            problem: Problem,
            input_data: str,
            expected_output: str,
            is_hidden: bool = False
    ) -> TestCase:
        test_case = TestCase(
            problem=problem,
            input_data=input_data,
            expected_output=expected_output,
            is_hidden=is_hidden
        )
        return TestCaseRepository.save(test_case)

    @staticmethod
    def get_test_cases_for_problem(problem_id: uuid.UUID):
        return TestCase.objects.filter(problem_id=problem_id)

    @staticmethod
    def get_by_id(test_case_id: uuid.UUID):
        return TestCase.objects.get(id=test_case_id)
