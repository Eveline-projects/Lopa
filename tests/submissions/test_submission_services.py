import pytest
from django.core.exceptions import ValidationError
from apps.submissions.services import SubmissionService
from apps.submissions.models import Submission


@pytest.mark.django_db
class TestSubmissionService:
    @pytest.fixture
    def services(self):
        return SubmissionService()

    def test_create_submission_should_set_correct_fields(self, services, user, problem):
        new_submission = services.create_submission(
            user=user,
            problem=problem,
            code='print("Hello World")',
        )
        assert new_submission.user == user
        assert new_submission.problem == problem
        assert new_submission.code == 'print("Hello World")'
        assert new_submission.status == Submission.Status.PENDING

    def test_create_submission_with_valid_data_should_succeed(self, services, user, problem):
        code = 'print("Hello World")'

        submission = services.create_submission(
            user=user,
            problem=problem,
            code=code
        )

        assert submission.id is not None
        assert submission.code == code
        assert submission.status == Submission.Status.PENDING

    def test_create_submission_should_raise_error_when_user_is_missing(self, services, problem):
        with pytest.raises(Exception):
            services.create_submission(
                user=None,
                problem=problem,
                code='print(1)'
            )

    def test_create_submission_should_not_save_on_empty_code(self, services, user, problem):
        initial_count = Submission.objects.count()

        with pytest.raises(ValidationError):
            services.create_submission(user=user, problem=problem, code=" ")

        assert Submission.objects.count() == initial_count

    def test_create_submission_should_raise_error_on_invalid_status(self, services, user, problem):
        with pytest.raises(ValidationError):
            services.create_submission(
                user=user,
                problem=problem,
                code='print("Hello World")',
                status='SUPER_INVALID_STATUS'
            )
