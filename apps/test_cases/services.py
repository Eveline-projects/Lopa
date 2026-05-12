import logging
import uuid
from uuid import UUID
from django.db.models import QuerySet

from apps.problems.repositories import ProblemRepository
from apps.problems.exceptions import ProblemNotFound

from .models import TestCase
from .repositories import TestCaseRepository

logger = logging.getLogger(__name__)


class TestCaseService:
    @staticmethod
    def create_test_case(
        problem_id: UUID,
        input_data: str,
        expected_output: str,
        is_hidden: bool = False,
    ) -> TestCase:

        problem = ProblemRepository.get_active_by_id(problem_id)
        if not problem:
            logger.warning(
                'test_case rejected problem not found problem_id=%s',
                problem_id,
            )
            raise ProblemNotFound('Problem not found')

        test_case = TestCaseRepository.create(
            problem=problem,
            input_data=input_data,
            expected_output=expected_output,
            is_hidden=is_hidden,
        )
        logger.info(
            'test_case created id=%s problem_id=%s is_hidden=%s',
            test_case.id,
            problem_id,
            is_hidden,
        )
        return test_case

    @staticmethod
    def get_test_cases_for_problem(
        problem_id: uuid.UUID,
    ) -> QuerySet[TestCase]:
        return TestCaseRepository.get_test_cases_for_problem(problem_id)

    @staticmethod
    def get_test_case_by_id(test_case_id: uuid.UUID) -> TestCase:
        test_case = TestCaseRepository.get_by_id(test_case_id)
        if not test_case:
            logger.warning('test_case not found id=%s', test_case_id)
            raise TestCase.DoesNotExist('TestCase {test_case_id} not found')
        return test_case
