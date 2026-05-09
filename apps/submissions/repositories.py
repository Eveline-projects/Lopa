from uuid import UUID
from django.db.models import QuerySet
from typing import Optional

from apps.problems.models import Problem
from apps.users.models import User
from apps.submissions.models import Submission


class SubmissionRepository:
    @staticmethod
    def save(submission: Submission):
        submission.full_clean()
        submission.save()
        return submission

    @staticmethod
    def create(
        user: User,
        problem: Problem,
        code: str,
        status: str = 'PENDING',
    ) -> Submission:
        submission = Submission(
            user=user,
            problem=problem,
            code=code,
            status=status,
        )
        return SubmissionRepository.save(submission)

    @staticmethod
    def get_by_id(submission_id: UUID) -> Optional[Submission]:
        try:
            return Submission.objects.get(id=submission_id)
        except Submission.DoesNotExist:
            return None

    @staticmethod
    def get_submissions_for_problem(problem_id: UUID) -> QuerySet[Submission]:
        return Submission.objects.filter(problem_id=problem_id).order_by(
            '-created_at'
        )

    @staticmethod
    def get_solved_subquery_for_user(user: User) -> QuerySet[Submission]:
        return Submission.objects.filter(
            user=user, status=Submission.Status.DONE
        )
