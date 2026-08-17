import logging

from celery import shared_task
from docker.errors import APIError, DockerException

from apps.submissions.models import Submission
from apps.submissions.status_services import SubmissionEvaluationService

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(APIError, DockerException, ConnectionError),
    retry_backoff=True,
    retry_kwargs={'max_retries': 3},
)
def evaluate_submission_task(self, submission_id: str) -> None:
    """
    Asynchronously fetches a submission from the database and triggers its evaluation.
    Accepts submission_id as a string due to Celery JSON serialization limits.
    """

    try:
        # Using string ID is safe; Django's ORM handles the conversion to UUID automatically
        submission = Submission.objects.get(id=submission_id)
        SubmissionEvaluationService.evaluate(submission)

    except Submission.DoesNotExist:
        logger.warning(
            f'Submission with ID {submission_id} was not found in the database.'
        )

    except Exception:
        logger.exception(
            'Celery caught unexpected error during evaluation',)
        raise
