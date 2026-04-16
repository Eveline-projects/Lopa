import pytest
from ninja.testing import TestClient

from apps.problems.api import router
from apps.problems.models import Problem

client = TestClient(router)


@pytest.mark.django_db
class TestProblemApi:
    def test_list_problems_should_return_only_active_problems(self):
        active_problem = Problem.objects.create(
            title="Active problem",
            description="Active description",
            difficulty="easy",
            category="arrays",
            is_active=True,
        )
        Problem.objects.create(
            title="Inactive problem",
            description="Inactive description",
            difficulty="medium",
            category="strings",
            is_active=False,
        )

        response = client.get('/')

        assert response.status_code == 200
        data = response.json()

        assert len(data) == 1
        assert data[0]["id"] == str(active_problem.id)
        assert data[0]["title"] == "Active problem"
        assert data[0]["description"] == "Active description"
        assert data[0]["difficulty"] == "easy"
        assert data[0]["category"] == "arrays"
        assert data[0]["is_active"] is True

    def test_get_problem_should_return_single_active_problem(self):
        problem = Problem.objects.create(
            title="Binary Search",
            description="Find target in sorted array",
            difficulty="medium",
            category="algorithms",
            is_active=True,
        )

        response = client.get(f"/{problem.id}/")

        assert response.status_code == 200
        data = response.json()

        assert data["id"] == str(problem.id)
        assert data["title"] == "Binary Search"
        assert data["description"] == "Find target in sorted array"
        assert data["difficulty"] == "medium"
        assert data["category"] == "algorithms"
        assert data["is_active"] is True

    def test_get_problem_should_return_404_for_inactive_problem(self):
        problem = Problem.objects.create(
            title="Hidden problem",
            description="Should not be available",
            difficulty="easy",
            category="arrays",
            is_active=False,
        )

        response = client.get(f"/{problem.id}/")

        assert response.status_code == 404
        assert response.json()["detail"] == "Problem not found"

    def test_get_problem_should_return_404_for_nonexistent_problem(self):
        response = client.get("/11111111-1111-1111-1111-111111111111/")

        assert response.status_code == 404
        assert response.json()["detail"] == "Problem not found"

    def test_create_problem_should_create_problem_and_return_201(self):
        payload = {
            "title": "Two Sum",
            "description": "Return indices of two numbers that add up to target",
            "difficulty": "easy",
            "category": "arrays",
        }

        response = client.post("/", json=payload)

        assert response.status_code == 201
        data = response.json()

        assert data["title"] == payload["title"]
        assert data["description"] == payload["description"]
        assert data["difficulty"] == payload["difficulty"]
        assert data["category"] == payload["category"]
        assert data["is_active"] is True

        assert Problem.objects.count() == 1
        assert Problem.objects.first().title == "Two Sum"
