import pytest
import uuid

from ninja.testing import TestClient

from apps.submissions.api import router
from apps.submissions.models import Submission

client = TestClient(router)


@pytest.mark.django_db
class TestSubmissionApi:
    def test_get_submission_should_return_200(self, user, problem):
        submission = Submission.objects.create(
            user=user, problem=problem, code='[1,2,3]', status='PENDING'
        )

        response = client.get(f'/submissions/{submission.id}/')

        assert response.status_code == 200

    def test_get_submission_should_return_submission_data(self, user, problem):
        submission = Submission.objects.create(
            user=user, problem=problem, code='[1,2,3]', status='PENDING'
        )

        response = client.get(f'/submissions/{submission.id}/')

        data = response.json()

        assert data['id'] == str(submission.id)
        assert data['problem_id'] == str(problem.id)
        assert data['user_id'] == user.id

    def test_get_submission_should_return_404_for_non_existing_submission(
        self,
    ):
        non_existent_id = uuid.uuid4()

        response = client.get(f'/submissions/{non_existent_id}/')

        assert response.status_code == 404
        assert response.json()['detail'] == 'Submission not found'

    def test_create_submission_should_return_201(
        self, user, problem, monkeypatch
    ):
        monkeypatch.setattr(
            'apps.submissions.status_services.SubmissionEvaluationService.evaluate',
            lambda x: None,
        )
        payload = {
            'code': '[1,2,3]',
        }

        response = client.post(
            f'/problems/{problem.id}/submissions/', json=payload, user=user
        )

        assert response.status_code == 201
        data = response.json()
        assert data['problem_id'] == str(problem.id)
        assert data['status'] == 'PENDING'
        assert data['created_at'] is not None

    def test_create_submission_should_return_404_when_problem_does_not_exist(
        self, user
    ):
        payload = {
            'code': '[1,2,3]',
        }
        non_existent_problem_id = uuid.uuid4()

        response = client.post(
            f'/problems/{non_existent_problem_id}/submissions/',
            json=payload,
            user=user,
        )

        assert response.status_code == 404
        assert response.json()['detail'] == 'Problem not found'

    def test_should_create_submission_in_database(self, user, problem):
        payload = {
            'code': '[1,2,3]',
        }

        response = client.post(
            f'/problems/{problem.id}/submissions/', json=payload, user=user
        )

        assert response.status_code == 201
        assert Submission.objects.count() == 1

        submission = Submission.objects.first()
        assert submission.user == user
        assert submission.problem == problem
        assert submission.code == '[1,2,3]'

    def test_get_submissions_for_problem_should_return_submissions_in_order(
        self, user, problem
    ):
        first_submission = Submission.objects.create(
            user=user, problem=problem, code='[1,2,3]', status='PENDING'
        )
        second_submission = Submission.objects.create(
            user=user, problem=problem, code='[4,5,6]', status='PENDING'
        )

        response = client.get(f'/problems/{problem.id}/submissions/')

        assert response.status_code == 200
        data = response.json()

        assert len(data) == 2
        assert data[0]['id'] == str(second_submission.id)
        assert data[1]['id'] == str(first_submission.id)

        assert data[0]['code'] == '[4,5,6]'
        assert data[1]['code'] == '[1,2,3]'

    def test_create_submission_with_empty_code_should_return_422(
        self, user, problem
    ):
        payload = {'problem_id': str(problem.id), 'code': '  '}

        response = client.post(
            f'/problems/{problem.id}/submissions/',
            json=payload,
            user=user,
        )

        assert response.status_code == 422
        assert response.json()['detail'] == 'Code cannot be empty'
