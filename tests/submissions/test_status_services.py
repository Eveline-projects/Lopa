import pytest
from unittest.mock import MagicMock

from apps.submissions.models import Submission
from apps.results.models import Result
from apps.submissions.status_services import (
    SubmissionStatusService,
    SubmissionEvaluationService,
)


@pytest.mark.django_db
class TestSubmissionStatusService:
    def test_submission_status_service_should_all_passed(self):
        results = [
            MagicMock(status=Result.Status.PASSED),
            MagicMock(status=Result.Status.PASSED),
        ]
        status = SubmissionStatusService.resolve(results)

        assert status == Submission.Status.DONE

    def test_submission_status_service_should_has_wrong_answer(self):
        results = [
            MagicMock(status=Result.Status.PASSED),
            MagicMock(status=Result.Status.WRONG_ANSWER),
        ]
        status = SubmissionStatusService.resolve(results)

        assert status == Submission.Status.WRONG_ANSWER

    def test_submission_status_service_should_has_runtime_error(self):
        results = [MagicMock(status=Result.Status.RUNTIME_ERROR)]
        status = SubmissionStatusService.resolve(results)

        assert status == Submission.Status.ERROR


@pytest.mark.django_db
class TestSubmissionEvaluationService:
    def test_submission_evaluate_service_should_all_passed(
        self, test_case, submission
    ):
        submission.code = test_case.expected_output
        result = SubmissionEvaluationService.evaluate(submission)

        assert result.status == Submission.Status.DONE
        assert Result.objects.filter(submission=submission).count() == 1
        assert all(
            r.status == Result.Status.PASSED for r in submission.results.all()
        )

    def test_submission_evaluate_service_should_wrong_answer(
        self, submission, test_case
    ):

        test_case.problem = submission.problem
        test_case.save()

        submission.code = "print('Hello World')"
        result = SubmissionEvaluationService.evaluate(submission)

        assert result.status == Submission.Status.WRONG_ANSWER
        assert any(
            r.status == Result.Status.WRONG_ANSWER
            for r in submission.results.all()
        )
