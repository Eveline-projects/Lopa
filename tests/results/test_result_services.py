import pytest
from django.core.exceptions import ValidationError
from apps.results.services import ResultService
from apps.results.models import Result


@pytest.mark.django_db
class TestResultService:
    @pytest.fixture
    def services(self):
        return ResultService()

    def test_create_result_should_set_correct_fields(self, services, submission, test_case):
        result = services.create_result(
            submission=submission,
            test_case=test_case,
            actual_output='123',
            execution_time=0.0,
        )

        assert Result.objects.count() == 1
        assert result.submission == submission
        assert result.test_case == test_case
        assert result.actual_output == '123'
        assert result.execution_time == 0.0

    @pytest.mark.parametrize("valid_status", [
        Result.Status.PASSED,
        Result.Status.WRONG_ANSWER,
        Result.Status.TIME_LIMIT_EXCEEDED,
        Result.Status.RUNTIME_ERROR
    ])
    def test_update_result_with_all_valid_statuses_should_succeed(self, services, result, valid_status):
        updated = services.update_result(result=result, status=valid_status)

        assert updated.status == valid_status
        assert not Result.objects.filter(status=Result.Status.PENDING).exists()

    def test_create_result_should_not_save_to_db_on_validation_error(self, services, submission, test_case):
        initial_count = Result.objects.count()

        with pytest.raises(ValidationError):
            services.create_result(
                submission=submission,
                test_case=test_case,
                actual_output='123',
                execution_time=0.2,
                status='INVALID_STATUS_NAME'
            )

        assert Result.objects.count() == initial_count

    def test_create_result_with_empty_output_should_succeed(self, services, submission, test_case):
        result = services.create_result(
            submission=submission,
            test_case=test_case,
            actual_output=''
        )

        assert result.actual_output == ''
        assert Result.objects.count() == 1

    def test_create_result_should_start_as_pending(self, services, submission, test_case):
        result = services.create_result(submission=submission, test_case=test_case)

        assert result.status == Result.Status.PENDING
        assert result.actual_output == ""
        assert result.execution_time == 0.0

    def test_update_result_should_change_status_and_output(self, services, result):
        updated = services.update_result(
            result=result,
            status=Result.Status.WRONG_ANSWER,
            actual_output='Expected 4, got 5',
            execution_time=0.25
        )

        assert updated.status == Result.Status.WRONG_ANSWER
        assert updated.actual_output == 'Expected 4, got 5'
        assert updated.execution_time == 0.25

    def test_update_result_should_persist_in_db(self, services, result):
        new_output = 'Final engine output'
        services.update_result(result=result, actual_output=new_output)
        result.refresh_from_db()

        assert result.actual_output == new_output

    @pytest.mark.parametrize('invalid_status', ["WRONG", "HACKER_STATUS", "123"])
    def test_update_result_should_raise_error_on_invalid_status(self, services, result, invalid_status):
        with pytest.raises(ValidationError, match='Invalid status level'):
            services.update_result(result=result, status=invalid_status)
