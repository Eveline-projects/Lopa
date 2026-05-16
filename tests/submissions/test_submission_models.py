from apps.submissions.models import Submission
import pytest


@pytest.mark.django_db
class TestSubmissionModel:
    def test_submission_should_be_linked_to_correct_user(self, submission):
        assert submission.user.username == 'Adam'

    def test_submission_should_be_linked_to_correct_problem(
        self, submission, problem
    ):
        assert submission.problem == problem

    def test_submission_should_store_submitted_code(self, submission):
        assert submission.code == 'print("Hello World")'

    def test_submission_should_have_pending_status_by_default(
        self, submission
    ):
        assert Submission.objects.count() == 1
        assert submission.status == Submission.Status.PENDING
