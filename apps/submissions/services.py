import logging
from uuid import UUID

from django.core.exceptions import ValidationError
from django.db.models import QuerySet

from .models import Submission
from apps.users.models import User
from .repositories import SubmissionRepository
from apps.problems.repositories import ProblemRepository
from apps.problems.exceptions import ProblemNotFound

logger = logging.getLogger(__name__)

STATUS_CHOICES_SUBMISSION = Submission.Status.values


class SubmissionService:
    @staticmethod
    def create_submission(
        user: User, problem_id: UUID, code: str, status=None
    ) -> Submission:
        if status is None:
            status = Submission.Status.PENDING

        if not code.strip():
            raise ValidationError('Code cannot be empty')

        problem = ProblemRepository.get_active_by_id(problem_id)
        if not problem:
            logger.warning(
                'submission rejected problem not found problem_id=%s user_id=%s',
                problem_id,
                user.id,
            )
            raise ProblemNotFound('Problem not found')

        submission = SubmissionRepository.create(
            user=user,
            problem=problem,
            code=code,
            status=status,
        )
        logger.info(
            'submission created id=%s problem_id=%s user_id=%s status=%s',
            submission.id,
            problem_id,
            user.id,
            submission.status,
        )

        return submission

    @staticmethod
    def get_submission_by_id(submission_id: UUID) -> Submission:
        submission = SubmissionRepository.get_by_id(submission_id)

        if not submission:
            logger.warning('submission not found id=%s', submission_id)
            raise Submission.DoesNotExist(
                f'Submission {submission_id} not found'
            )

        return submission

    @staticmethod
    def get_submissions_for_problem(problem_id: UUID) -> QuerySet[Submission]:
        return SubmissionRepository.get_submissions_for_problem(problem_id)
