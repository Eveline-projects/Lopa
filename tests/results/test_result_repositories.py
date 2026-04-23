import pytest
from uuid import UUID

from apps.results.models import Result
from apps.results.repositories import ResultRepository


@pytest.mark.django_db
class TestResultRepository:
    def test_get_by_id_should_return_result(self, result):
        found_result = ResultRepository.get_by_id(result.id)

        assert found_result.id == result.id
        assert found_result.submission_id == result.submission_id
        assert found_result.test_case_id == result.test_case_id
        assert found_result.status == result.status

    def test_get_results_for_submission_should_return_only_submission_results(
        self, submission, other_result, result
    ):
        results = ResultRepository.get_results_for_submission(submission.id)

        assert results.count() == 1
        assert result in results
        assert other_result not in results

    def test_create_should_create_result_with_given_data(
        self, submission, test_case
    ):
        created = ResultRepository.create(
            submission=submission,
            test_case=test_case,
            actual_output='42',
            execution_time=0.12,
            status=Result.Status.PENDING,
        )

        assert created.id is not None
        assert created.submission == submission
        assert created.test_case == test_case
        assert created.actual_output == '42'
        assert created.execution_time == 0.12
        assert created.status == Result.Status.PENDING

    def test_get_by_id_should_raise_does_not_exist_for_nonexistent_result(
        self,
    ):
        nonexistent_id = UUID('11111111-1111-1111-1111-111111111111')

        with pytest.raises(Result.DoesNotExist):
            ResultRepository.get_by_id(nonexistent_id)
