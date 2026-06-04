from unittest.mock import patch
import pytest
from apps.submissions.tasks import evaluate_submission_task
from apps.submissions.models import Submission


@pytest.mark.django_db
@patch('apps.submissions.status_services.SubmissionEvaluationService.evaluate')
class TestSubmissionTasks:
    def test_evaluate_submission_task_should_call_evaluation_service(
        self, mock_evaluate, problem, user
    ):
        submission = Submission.objects.create(
            user=user, problem=problem, code="print('Hello')", status='PENDING'
        )

        evaluate_submission_task(str(submission.id))

        mock_evaluate.assert_called_once_with(submission)

    def test_evaluate_submission_task_should_handle_does_not_exist_gracefully(
        self, mock_evaluate
    ):
        fake_uuid = '00000000-0000-0000-0000-000000000000'

        evaluate_submission_task(fake_uuid)

        mock_evaluate.assert_not_called()
