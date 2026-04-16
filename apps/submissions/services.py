from django.core.exceptions import ValidationError
from .models import Submission
from apps.problems.models import Problem
from apps.users.models import User

STATUS_CHOICES_SUBMISSION = Submission.Status.values


class SubmissionService:
    @staticmethod
    def create_submission(
            user: User,
            problem: Problem,
            code: str,
            status=None
    ) -> Submission:
        if status is None:
            status = Submission.Status.PENDING

        if not code.strip():
            raise ValidationError('Code cannot be empty')

        submission = Submission.objects.create(
            user=user,
            problem=problem,
            code=code,
            status=status,
        )
        submission.full_clean()
        submission.save()
        return submission
