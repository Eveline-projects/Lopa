import pytest
from django.core.exceptions import ValidationError
from apps.problems.models import Problem
from apps.problems.repositories import ProblemRepository


@pytest.mark.django_db
class TestProblemRepository:
    def test_get_active_by_id_should_return_only_active_problem(
        self, problem: Problem
    ):
        assert problem.is_active is True

        found = ProblemRepository.get_active_by_id(problem.id)

        assert found == problem

    def test_get_active_by_id_should_raise_for_inactive_problem(
        self, problem: Problem
    ):
        problem.is_active = False
        problem.save()

        problem = ProblemRepository.get_active_by_id(problem.id)

        assert problem is None

    def test_get_by_id_should_return_active_or_inactive_problem(
        self, problem: Problem
    ):
        inactive = Problem.objects.create(
            title='Inactive problem',
            description='Inactive',
            difficulty='Easy',
            category='arrays',
            is_active=False,
        )

        assert ProblemRepository.get_by_id(problem.id) == problem
        assert ProblemRepository.get_by_id(inactive.id) == inactive

    def test_list_active_should_return_only_active_problems(self):
        active = Problem.objects.create(
            title='Active',
            description='Active',
            difficulty='easy',
            category='arrays',
            is_active=True,
        )
        Problem.objects.create(
            title='Inactive',
            description='Inactive',
            difficulty='medium',
            category='strings',
            is_active=False,
        )

        result = ProblemRepository.list_active()

        assert len(result) == 1
        assert result[0] == active

    def test_save_should_run_full_clean(self):
        problem = Problem(
            title='Invalid',
            description='Too short',
            difficulty='invalid_difficulty',
            category='arrays',
            is_active=True,
        )

        with pytest.raises(ValidationError):
            ProblemRepository.save(problem)

    def test_update_should_only_allow_whitelisted_fields(self):
        problem = Problem.objects.create(
            title='Original',
            description='Original',
            difficulty='easy',
            category='arrays',
            is_active=True,
        )

        allowed_update = {'title': 'New title', 'difficulty': 'medium'}
        updated = ProblemRepository.update(problem, **allowed_update)
        assert updated.title == 'New title'
        assert updated.difficulty == 'medium'

        with pytest.raises(ValueError):
            ProblemRepository.update(problem, disallowed_field='oops')
