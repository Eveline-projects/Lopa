from unittest.mock import MagicMock, patch

import pytest

from apps.results.models import Result
from apps.submissions.models import Submission
from apps.submissions.status_services import (
    SubmissionEvaluationService,
    SubmissionStatusService,
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
@patch('apps.submissions.status_services.run_code_in_sandbox')
class TestSubmissionEvaluationService:
    def test_submission_evaluate_service_should_all_passed(
        self, mock_sandbox, test_case, submission
    ):
        test_case.problem = submission.problem
        test_case.expected_output = 'Hello'
        test_case.save()

        mock_sandbox.return_value = ('Hello', 0.1, Result.Status.PASSED)

        result = SubmissionEvaluationService.evaluate(submission)

        assert result.status == Submission.Status.DONE
        assert Result.objects.filter(submission=submission).count() == 1
        assert all(
            r.status == Result.Status.PASSED for r in submission.results.all()
        )

    def test_submission_evaluate_service_should_wrong_answer(
        self, mock_sandbox, submission, test_case
    ):

        test_case.problem = submission.problem
        test_case.expected_output = 'Expected Output'
        test_case.save()

        mock_sandbox.return_value = (
            'Completely Different Output',
            0.1,
            Result.Status.PASSED,
        )
        result = SubmissionEvaluationService.evaluate(submission)

        assert result.status == Submission.Status.WRONG_ANSWER
        assert any(
            r.status == Result.Status.WRONG_ANSWER
            for r in submission.results.all()
        )

    def test_submission_evaluate_service_should_timeout(
        self, mock_sandbox, submission, test_case
    ):
        test_case.problem = submission.problem
        test_case.save()

        mock_sandbox.return_value = (
            'Time Limit Exceeded',
            2.0,
            Result.Status.TIME_LIMIT_EXCEEDED,
        )

        result = SubmissionEvaluationService.evaluate(submission)

        assert result.status == Submission.Status.ERROR
        assert any(
            r.status == Result.Status.TIME_LIMIT_EXCEEDED
            for r in submission.results.all()
        )
