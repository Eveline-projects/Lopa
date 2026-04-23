import pytest
from ninja.testing import TestClient

from apps.results.api import router

client = TestClient(router)


@pytest.mark.django_db
class TestResultApi:
    def test_get_result_should_return_single_result(self, result):
        response = client.get(f'/results/{result.id}/')

        assert response.status_code == 200
        data = response.json()

        assert data['id'] == str(result.id)
        assert data['submission_id'] == str(result.submission_id)
        assert data['test_case_id'] == str(result.test_case_id)
        assert data['status'] == result.status
        assert data['actual_output'] == result.actual_output
        assert data['execution_time'] == result.execution_time

    def test_get_result_should_return_404_for_nonexistent_result(self):
        response = client.get('/results/11111111-1111-1111-1111-111111111111/')

        assert response.status_code == 404
        assert response.json()['detail'] == 'Result does not exist'

    def test_get_results_for_submission_should_return_only_submission_results(
        self, submission, result, other_result
    ):
        response = client.get(f'/submissions/{submission.id}/results/')

        assert response.status_code == 200
        data = response.json()

        assert len(data) == 1
        assert data[0]['id'] == str(result.id)
        assert data[0]['submission_id'] == str(submission.id)
        assert data[0]['test_case_id'] == str(result.test_case_id)

    def test_get_results_for_submission_should_return_empty_list_when_no_results(
        self, submission
    ):
        response = client.get(f'/submissions/{submission.id}/results/')

        assert response.status_code == 200
        assert response.json() == []
