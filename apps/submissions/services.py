from uuid import UUID

from django.core.exceptions import ValidationError
from django.db.models import QuerySet

from .models import Submission
from apps.problems.models import Problem
from apps.users.models import User
from .repositories import SubmissionRepository
from apps.problems.repositories import ProblemRepository
from apps.problems.exceptions import ProblemNotFound

STATUS_CHOICES_SUBMISSION = Submission.Status.values


class SubmissionService:
    @staticmethod
    def create_submission(
            user: User,
            problem_id: UUID,
            code: str,
            status=None
    ) -> Submission:
        if status is None:
            status = Submission.Status.PENDING

        if not code.strip():
            raise ValidationError('Code cannot be empty')

        try:
            problem = ProblemRepository.get_active_by_id(problem_id)
        except Problem.DoesNotExist as exc:
            raise ProblemNotFound('Problem not found') from exc

        return SubmissionRepository.create(
            user=user,
            problem=problem,
            code=code,
            status=status,
        )

    @staticmethod
    def get_submission_by_id(submission_id: UUID) -> Submission:
        return SubmissionRepository.get_by_id(submission_id)

    @staticmethod
    def get_submissions_for_problem(problem_id: UUID) -> QuerySet[Submission]:
        return SubmissionRepository.get_submissions_for_problem(problem_id)
