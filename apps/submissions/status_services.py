from apps.results.models import Result
from apps.results.repositories import ResultRepository
from .models import Submission
from .repositories import SubmissionRepository


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
        test_cases = submission.problem.test_cases.all().order_by('id')

        if not test_cases.exists():
            submission.status = Submission.Status.ERROR
            return SubmissionRepository.save(submission)

        created_results = []

        for test_case in test_cases:
            code = submission.code.strip()
            normalized_code = code.lower()
            expected_output = test_case.expected_output.strip()

            if normalized_code == '__force_runtime_error__':
                result_status = Result.Status.RUNTIME_ERROR
                actual_output = 'Runtime Error: Forced via magic string'
            elif normalized_code == '__force_timeout__':
                result_status = Result.Status.TIME_LIMIT_EXCEEDED
                actual_output = 'Time Limit Exceeded'

            elif code == expected_output:
                result_status = Result.Status.PASSED
                actual_output = code
            else:
                result_status = Result.Status.WRONG_ANSWER
                actual_output = code

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

        submission.status = SubmissionStatusService.resolve(created_results)
        return SubmissionRepository.save(submission)
