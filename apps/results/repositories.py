from uuid import UUID
from django.db.models import QuerySet
from typing import Optional

from .models import Result
from apps.test_cases.models import TestCase
from apps.submissions.models import Submission


class ResultRepository:
    @staticmethod
    def save(result: Result) -> Result:
        result.full_clean()
        result.save()
        return result

    @staticmethod
    def create(
        submission: Submission,
        test_case: TestCase,
        actual_output: str,
        execution_time: float,
        status: str = Result.Status.PENDING,
    ) -> Result:
        result = Result(
            submission=submission,
            test_case=test_case,
            actual_output=actual_output,
            execution_time=execution_time,
            status=status,
        )
        return ResultRepository.save(result)

    @staticmethod
    def get_by_id(result_id: UUID) -> Optional[Result]:
        try:
            return Result.objects.get(id=result_id)
        except Result.DoesNotExist:
            return None

    @staticmethod
    def get_results_for_submission(submission_id: UUID) -> QuerySet[Result]:
        return Result.objects.filter(submission_id=submission_id)
