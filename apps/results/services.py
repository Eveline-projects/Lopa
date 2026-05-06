from uuid import UUID
from django.core.exceptions import ValidationError
from django.db.models import QuerySet

from .models import Result
from .repositories import ResultRepository
from apps.test_cases.models import TestCase
from apps.submissions.models import Submission

STATUS_CHOICES_RESULT = Result.Status.values


class ResultService:
    @staticmethod
    def create_result(
        submission: Submission,
        test_case: TestCase,
        actual_output: str = '',
        execution_time: float = 0.0,
        status: str | None = None,
    ) -> Result:
        if status is not None and status not in STATUS_CHOICES_RESULT:
            raise ValidationError('Invalid status level')

        return ResultRepository.create(
            submission=submission,
            test_case=test_case,
            status=status or Result.Status.PENDING,
            actual_output=actual_output,
            execution_time=execution_time,
        )

    @staticmethod
    def update_result(
        result: Result,
        status: str | None = None,
        actual_output: str | None = None,
        execution_time: float | None = None,
    ) -> Result:
        if status is not None and status not in STATUS_CHOICES_RESULT:
            raise ValidationError('Invalid status level')

        if status is not None:
            result.status = status
        if actual_output is not None:
            result.actual_output = actual_output
        if execution_time is not None:
            result.execution_time = execution_time

        return ResultRepository.save(result)

    @staticmethod
    def get_results_for_submission(
        submission_id: UUID, user
    ) -> QuerySet[Result]:
        return ResultRepository.get_results_for_submission(submission_id, user)

    @staticmethod
    def get_result_by_id(result_id: UUID) -> Result:
        result = ResultRepository.get_by_id(result_id)

        if not result:
            raise Result.DoesNotExist(f'Result with id {result_id} not found')

        return result
