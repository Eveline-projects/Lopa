import os
import signal
import sys
import logging
import tempfile
import time
import subprocess
from django.conf import settings
from apps.results.models import Result
from apps.results.repositories import ResultRepository
from .models import Submission
from .repositories import SubmissionRepository

TIMEOUT_LIMIT = getattr(settings, 'SUBMISSION_TIMEOUT', 2.0)
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
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py') as fp:
                    fp.write(submission.code.strip())
                    fp.flush()

                    expected_output = test_case.expected_output.strip()

                    actual_output = ''
                    result_status = Result.Status.RUNTIME_ERROR
                    execution_time = 0.0

                    try:
                        process = subprocess.Popen(
                            [sys.executable, fp.name],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                            start_new_session=True,
                        )

                        try:
                            start_time = time.perf_counter()

                            stdout_data, stderr_data = process.communicate(
                                input=test_case.input_data,
                                timeout=TIMEOUT_LIMIT,
                            )

                            execution_time = time.perf_counter() - start_time

                            stdout_data = (
                                stdout_data[:MAX_OUTPUT_SIZE]
                                if stdout_data
                                else ''
                            )
                            stderr_data = (
                                stderr_data[:MAX_OUTPUT_SIZE]
                                if stderr_data
                                else ''
                            )

                            if process.returncode == 0:
                                actual_output = stdout_data.strip()

                                normalized_actual = ' '.join(
                                    actual_output.split()
                                )
                                normalized_expected = ' '.join(
                                    expected_output.strip().split()
                                )

                                if normalized_actual == normalized_expected:
                                    result_status = Result.Status.PASSED
                                else:
                                    result_status = Result.Status.WRONG_ANSWER
                            else:
                                actual_output = stderr_data.strip()
                                result_status = Result.Status.RUNTIME_ERROR

                        except subprocess.TimeoutExpired:
                            try:
                                os.killpg(
                                    os.getpgid(process.pid), signal.SIGKILL
                                )
                            except ProcessLookupError:
                                pass

                            execution_time = time.perf_counter() - start_time
                            stdout_data, stderr_data = process.communicate()
                            actual_output = 'Time Limit Exceeded'
                            result_status = Result.Status.TIME_LIMIT_EXCEEDED

                    except Exception as engine_err:
                        logger.error('Execution engine error: %s', engine_err)
                        actual_output = str(engine_err)
                        result_status = Result.Status.RUNTIME_ERROR

                    result = ResultRepository.create(
                        submission=submission,
                        test_case=test_case,
                        actual_output=actual_output,
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
            raise e
