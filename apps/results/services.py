import logging
from uuid import UUID
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from .models import Result
from .repositories import ResultRepository
from apps.test_cases.models import TestCase
from apps.submissions.models import Submission

logger = logging.getLogger(__name__)

STATUS_CHOICES_RESULT = Result.Status.values

User = get_user_model()


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
            logger.warning('Result creation failed: invalid status=%s', status)
            raise ValidationError('Invalid status level')

        result = ResultRepository.create(
            submission=submission,
            test_case=test_case,
            status=status or Result.Status.PENDING,
            actual_output=actual_output,
            execution_time=execution_time,
        )
        logger.debug(
            'result created id=%s submission_id=%s test_case_id=%s status=%s',
            result.id,
            submission.id,
            test_case.id,
            result.status,
        )
        return result

    @staticmethod
    def update_result(
        result: Result,
        status: str | None = None,
        actual_output: str | None = None,
        execution_time: float | None = None,
    ) -> Result:
        if status is not None and status not in STATUS_CHOICES_RESULT:
            logger.warning(
                'Result update failed: invalid status=%s id=%s',
                status,
                result.id,
            )
            raise ValidationError('Invalid status level')

        changed = []
        if status is not None:
            result.status = status
            changed.append('status')
        if actual_output is not None:
            result.actual_output = actual_output
            changed.append('actual_output')
        if execution_time is not None:
            result.execution_time = execution_time
            changed.append('execution_time')

        saved = ResultRepository.save(result)
        logger.info(
            'result updated id=%s fields=%s status=%s',
            saved.id,
            changed,
            saved.status,
        )
        return saved

    @staticmethod
    def get_results_for_submission(
        submission_id: UUID, user: User
    ) -> QuerySet[Result]:
        return ResultRepository.get_results_for_submission(submission_id, user)

    @staticmethod
    def get_result_by_id(result_id: UUID, user: User) -> Result:
        result = ResultRepository.get_by_id(result_id, user)

        if not result:
            logger.warning('result not found id=%s', result_id, user.id)
            raise Result.DoesNotExist(f'Result with id {result_id} not found')

        return result
