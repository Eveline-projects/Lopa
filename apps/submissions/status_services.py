import logging
import tempfile
import subprocess
from apps.results.models import Result
from apps.results.repositories import ResultRepository
from .models import Submission
from .repositories import SubmissionRepository

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
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py') as fp:
                    fp.write(submission.code.strip())
                    fp.flush()

                    expected_output = test_case.expected_output.strip()

                    try:
                        process = subprocess.run(
                            ['python', fp.name],
                            input=test_case.input_data,
                            capture_output=True,
                            text=True,
                            timeout=2.0,
                        )

                        if process.returncode == 0:
                            actual_output = process.stdout.strip()
                            if actual_output == expected_output:
                                result_status = Result.Status.PASSED
                            else:
                                result_status = Result.Status.WRONG_ANSWER
                        else:
                            actual_output = process.stderr.strip()
                            result_status = Result.Status.RUNTIME_ERROR

                    except subprocess.TimeoutExpired:
                        actual_output = 'Time Limit Exceeded'
                        result_status = Result.Status.TIME_LIMIT_EXCEEDED

                    result = ResultRepository.create(
                        submission=submission,
                        test_case=test_case,
                        actual_output=actual_output,
                        execution_time=0.1
                        if result_status == Result.Status.PASSED
                        else 0.5,
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
            raise e
