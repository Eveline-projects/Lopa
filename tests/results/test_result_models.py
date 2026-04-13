import uuid
import pytest
from apps.results.models import Result


@pytest.mark.django_db
class TestResultService:
    def test_result_id_should_be_a_valid_uuid(self, result):
        assert isinstance(result.id, uuid.UUID)

    def test_result_should_be_linked_to_correct_submission(self, result, submission):
        assert result.submission == submission

    def test_result_should_be_linked_to_correct_test_case(self, result, test_case):
        assert result.test_case == test_case

    def test_result_should_have_pending_status_by_default(self, result):
        assert result.status == Result.Status.PENDING

    def test_result_should_store_actual_output_correctly(self, result):
        assert result.actual_output == '123'

    def test_result_should_have_valid_execution_time(self, result):
        assert isinstance(result.execution_time, float)
        assert result.execution_time == 0.2

    def test_submission_related_manager_should_access_results(self, submission, result):
        assert submission.results.count() == 1
        assert submission.results.first() == result

    def test_result_string_representation(self, result):
        expected_string = f"Result {result.id} - {result.status}"
        assert str(result) == expected_string
