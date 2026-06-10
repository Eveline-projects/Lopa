import logging
from apps.results.models import Result
from apps.results.repositories import ResultRepository
from .models import Submission
from .repositories import SubmissionRepository
from apps.submissions.sandbox import run_code_in_sandbox


MAX_OUTPUT_SIZE = 64 * 1024

logger = logging.getLogger(__name__)


class SubmissionStatusService:
    @staticmethod
    def resolve(results: list[Result]) -> str:
        if not results:
            return Submission.Status.PENDING

        statuses = [result.status for result in results]

        if any(status == Result.Status.RUNTIME_ERROR for status in statuses):
            return Submission.Status.ERROR

        if any(
            status == Result.Status.TIME_LIMIT_EXCEEDED for status in statuses
        ):
            return Submission.Status.ERROR

        if any(status == Result.Status.WRONG_ANSWER for status in statuses):
            return Submission.Status.WRONG_ANSWER

        if all(status == Result.Status.PASSED for status in statuses):
            return Submission.Status.DONE

        return Submission.Status.PENDING


class SubmissionEvaluationService:
    @staticmethod
    def evaluate(submission: Submission) -> Submission:
        logger.info(
            'Starting submission evaluation id=%s problem_id=%s',
            submission.id,
            submission.problem_id,
        )
        test_cases = list(submission.problem.test_cases.all().order_by('id'))

        if not test_cases:
            submission.status = Submission.Status.ERROR
            saved = SubmissionRepository.save(submission)
            logger.warning(
                'submission evaluated no test_cases id=%s status=%s',
                saved.id,
                saved.status,
            )
            return saved

        created_results = []

        try:
            for test_case in test_cases:
                expected_output = test_case.expected_output.strip()

                actual_output, execution_time, result_status = (
                    run_code_in_sandbox(
                        submission.code.strip(), test_case.input_data
                    )
                )

                if result_status == Result.Status.PASSED:
                    normalized_actual = ' '.join(actual_output.split())
                    normalized_expected = ' '.join(expected_output.split())

                    if normalized_actual != normalized_expected:
                        result_status = Result.Status.WRONG_ANSWER

                result = ResultRepository.create(
                    submission=submission,
                    test_case=test_case,
                    actual_output=actual_output[:MAX_OUTPUT_SIZE],
                    execution_time=execution_time,
                    status=result_status,
                )
                created_results.append(result)

                logger.debug(
                    'Evaluated test_case_id=%s for submission_id=%s status=%s',
                    test_case.id,
                    submission.id,
                    result_status,
                )

            submission.status = SubmissionStatusService.resolve(
                created_results
            )
            saved = SubmissionRepository.save(submission)
            logger.info(
                'submission evaluated id=%s status=%s test_cases=%d',
                saved.id,
                saved.status,
                len(created_results),
            )
            return saved

        except Exception as e:
            logger.error(
                'Fatal error during submission evaluation id=%s error=%s',
                submission.id,
                str(e),
                exc_info=True,
            )
            try:
                submission.status = Submission.Status.ERROR
                SubmissionRepository.save(submission)
            except Exception as db_error:
                logger.warning(
                    'Could not save error status to submission id=%s reason=%s',
                    submission.id,
                    str(db_error),
                )
            raise
