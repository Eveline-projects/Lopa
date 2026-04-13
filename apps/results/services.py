from django.core.exceptions import ValidationError
from .models import Result
from apps.test_cases.models import TestCase
from apps.submissions.models import Submission

STATUS_CHOICES_RESULT = Result.Status.values


class ResultService:
    def create_result(
            self,
            submission: Submission,
            test_case: TestCase,
            actual_output: str = "",
            execution_time: float = 0.0,
            status: str = None
    ) -> Result:

        result = Result(
            submission=submission,
            test_case=test_case,
            status=status or Result.Status.PENDING,
            actual_output=actual_output,
            execution_time=execution_time,
        )

        result.full_clean()

        result.save()
        return result

    def update_result(
            self,
            result: Result,
            status: str | None = None,
            actual_output: str | None = None,
            execution_time: float | None = None
    ) -> Result:
        if status is not None and status not in STATUS_CHOICES_RESULT:
            raise ValidationError('Invalid status level')

        if status is not None:
            result.status = status
        if actual_output is not None:
            result.actual_output = actual_output
        if execution_time is not None:
            result.execution_time = execution_time

        result.save()
        return result
