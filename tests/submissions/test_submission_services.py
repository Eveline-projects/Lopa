import pytest
from django.core.exceptions import ValidationError

from apps.submissions.models import Submission
from apps.submissions.services import SubmissionService


@pytest.mark.django_db
class TestSubmissionService:
    def test_create_submission_should_set_correct_fields(self, user, problem):
        new_submission = SubmissionService.create_submission(
            user=user,
            problem_id=problem.id,
            code='print("Hello World")',
        )
        assert new_submission.user == user
        assert new_submission.problem == problem
        assert new_submission.code == 'print("Hello World")'
        assert new_submission.status in Submission.Status.values

    def test_create_submission_with_valid_data_should_succeed(
        self, user, problem
    ):
        code = 'print("Hello World")'

        submission = SubmissionService.create_submission(
            user=user, problem_id=problem.id, code=code
        )

        assert submission.id is not None
        assert submission.code == code
        assert submission.status in Submission.Status.values

    def test_create_submission_should_raise_error_when_user_is_missing(
        self, problem
    ):
        with pytest.raises(ValueError):
            SubmissionService.create_submission(
                user=None, problem_id=problem, code='print(1)'
            )

    def test_create_submission_should_not_save_on_empty_code(
        self, user, problem
    ):
        initial_count = Submission.objects.count()

        with pytest.raises(ValidationError):
            SubmissionService.create_submission(
                user=user, problem_id=problem, code=' '
            )

        assert Submission.objects.count() == initial_count

    def test_create_submission_should_raise_error_on_invalid_status(
        self, user, problem
    ):
        with pytest.raises(ValidationError):
            SubmissionService.create_submission(
                user=user,
                problem_id=problem,
                code='print("Hello World")',
                status='SUPER_INVALID_STATUS',
            )
