import pytest
import uuid

from ninja.testing import TestClient

from apps.test_cases.api import router
from apps.test_cases.models import TestCase

client = TestClient(router)


@pytest.mark.django_db
class TestTestCaseApi:
    def test_get_test_case_returns_200(self, problem):
        test_case = TestCase.objects.create(
            problem=problem,
            input_data='[1,2,3]',
            expected_output='[0,1]',
            is_hidden=False,
        )

        response = client.get(f"/test-cases/{test_case.id}/")

        assert response.status_code == 200

    def test_get_test_case_returns_expected_data(self, problem):
        test_case = TestCase.objects.create(
            problem=problem,
            input_data='[1,2,3]',
            expected_output='[0,1]',
            is_hidden=False,
        )

        response = client.get(f"/test-cases/{test_case.id}/")
        data = response.json()

        assert data['id'] == str(test_case.id)
        assert data['problem_id'] == str(test_case.problem.id)
        assert data['input_data'] == '[1,2,3]'
        assert data['expected_output'] == '[0,1]'
        assert data['is_hidden'] is False

    def test_get_test_case_should_return_404_for_nonexistent_test_case(self):
        non_existent_id = uuid.uuid4()

        response = client.get(f"/test-cases/{non_existent_id}/")

        assert response.status_code == 404
        assert response.json()['detail'] == 'Test case does not exist'

    def test_create_test_case_returns_201(self, problem):
        payload = {
            'problem_id': str(problem.id),
            'input_data': '[1,2,3]',
            'expected_output': '[0,1]',
            'is_hidden': False,
        }

        response = client.post("/test-cases/", json=payload)

        assert response.status_code == 201

    def test_create_test_case_returns_created_data(self, problem):
        payload = {
            'problem_id': str(problem.id),
            'input_data': '[1,2,3]',
            'expected_output': '[0,1]',
            'is_hidden': False,
        }

        response = client.post("/test-cases/", json=payload)
        data = response.json()

        assert data["problem_id"] == payload["problem_id"]
        assert data["input_data"] == payload["input_data"]
        assert data["expected_output"] == payload["expected_output"]
        assert data["is_hidden"] is False
        assert "id" in data

    def test_create_test_case_persists_object_in_database(self, problem):
        payload = {
            'problem_id': str(problem.id),
            'input_data': '[1,2,3]',
            'expected_output': '[0,1]',
            'is_hidden': False,
        }

        response = client.post("/test-cases/", json=payload)

        assert response.status_code == 201
        assert TestCase.objects.count() == 1

        created_test_case = TestCase.objects.first()
        assert created_test_case is not None
        assert str(created_test_case.problem.id) == payload['problem_id']
        assert created_test_case.input_data == payload['input_data']
        assert created_test_case.expected_output == payload['expected_output']
        assert created_test_case.is_hidden == payload['is_hidden']

    def test_create_test_case_defaults_is_hidden_to_false(self, problem):
        payload = {
            'problem_id': str(problem.id),
            'input_data': '[1,2,3]',
            'expected_output': '[0,1]',
        }

        response = client.post("/test-cases/", json=payload)

        assert response.status_code == 201

        data = response.json()
        assert data["is_hidden"] is False

        created_test_case = TestCase.objects.get(id=data["id"])
        assert created_test_case.is_hidden is False

    def test_create_test_case_returns_404_when_problem_does_not_exist(self):
        payload = {
            'problem_id': str(uuid.uuid4()),
            'input_data': '[1,2,3]',
            'expected_output': '[0,1]',
            'is_hidden': False,
        }

        response = client.post("/test-cases/", json=payload)

        assert response.status_code == 404
        assert response.json()['detail'] == 'Problem not found'

    @pytest.mark.parametrize(
        'payload',
        [
            {
                'problem_id': None,
                'input_data': '   ',
                'expected_output': '[0,1]',
                'is_hidden': False,
            },
            {
                'problem_id': None,
                'input_data': '',
                'expected_output': '[0,1]',
                'is_hidden': False,
            },
        ],
        ids=['whitespace_input_data', 'empty_input_data'],
    )
    def test_create_test_case_returns_error_for_invalid_input_data(self, problem, payload):
        payload = {
            'problem_id': str(problem.id),
            'input_data': '   ',
            'expected_output': '[0,1]',
            'is_hidden': False,
        }

        response = client.post("/test-cases/", json=payload)
        assert response.status_code in [400, 422]

    def test_create_test_case_returns_error_for_invalid_expected_output(self, problem):
        payload = {
            'problem_id': str(problem.id),
            'input_data': '[1,2,3]',
            'expected_output': '  ',
            'is_hidden': False,
        }

        response = client.post('/test-cases/', json=payload)
        assert response.status_code == 422

    def test_get_test_cases_for_problem_should_return_test_cases_in_order(self, problem):
        first_test_case = TestCase.objects.create(
            problem=problem,
            input_data='in1',
            expected_output='out1',
        )
        second_test_case = TestCase.objects.create(
            problem=problem,
            input_data='in2',
            expected_output='out2',
        )

        response = client.get(f"/problems/{problem.id}/test-cases/")

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)
        assert len(data) == 2

        expected_order = sorted(
            [first_test_case, second_test_case],
            key=lambda test_case: str(test_case.id),
        )

        assert [item['id'] for item in data] == [str(test_case.id) for test_case in expected_order]
        assert [item['input_data'] for item in data] == [test_case.input_data for test_case in expected_order]
        assert [item['expected_output'] for item in data] == [test_case.expected_output for test_case in expected_order]
