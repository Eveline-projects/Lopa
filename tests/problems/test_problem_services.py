import pytest
from django.core.exceptions import ValidationError
from apps.problems.exceptions import ProblemNotFound
from apps.problems.services import ProblemService
from apps.problems.models import Problem


@pytest.mark.django_db
class TestProblemService:
    def test_create_problem_should_set_correct_fields(self):
        new_problem = ProblemService.create_problem(
            title='Easy Problem',
            description='Test',
            difficulty='easy',
            category='Test',
        )
        assert new_problem.title == 'Easy Problem'
        assert new_problem.description == 'Test'
        assert new_problem.difficulty == 'easy'
        assert new_problem.category == 'Test'
        assert new_problem.is_active is True

    def test_create_problem_should_create_record_in_db(self):
        new_problem = ProblemService.create_problem(
            title='Easy Problem',
            description='Test',
            difficulty='easy',
            category='Test',
        )
        assert Problem.objects.count() == 1
        assert new_problem.title == 'Easy Problem'

    def test_create_problem_should_raise_error_on_invalid_difficulty(self):
        with pytest.raises(ValidationError):
            ProblemService.create_problem(
                title='Test',
                description='Test',
                difficulty='invalid_level',
                category='Test',
            )

    def test_get_all_problems_should_returns_only_active_problems(self):
        Problem.objects.create(
            title='Active',
            description='Active description',
            difficulty='easy',
            category='arrays',
            is_active=True,
        )
        Problem.objects.create(
            title='Inactive',
            description='Inactive description',
            difficulty='easy',
            category='arrays',
            is_active=False,
        )

        problems = ProblemService.get_all_problems()

        assert problems.count() == 1
        assert problems.first().title == 'Active'
        assert problems.first().is_active is True

    def test_get_problem_by_id_should_returns_problem(self):
        problem = Problem.objects.create(title='Test Problem', is_active=True)
        result = ProblemService.get_problem_by_id(problem.id)

        assert result == problem
        assert result.title == 'Test Problem'

    def test_get_problem_by_id_should_raises_error_for_inactive_problem(self):
        inactive_problem = Problem.objects.create(
            title='Inactive Problem', is_active=False
        )

        with pytest.raises(ProblemNotFound, match='Problem not found'):
            ProblemService.get_problem_by_id(inactive_problem.id)

    def test_update_problem_should_update_only_provided_fields(
        self, problem: Problem
    ):
        old_difficulty = problem.difficulty
        new_title = 'New Title'

        ProblemService.update_problem(problem, title=new_title)

        problem.refresh_from_db()
        assert problem.title == new_title
        assert problem.difficulty == old_difficulty

    def test_update_problem_should_raise_error_on_invalid_difficulty(
        self, problem: Problem
    ):
        with pytest.raises(ValidationError):
            ProblemService.update_problem(
                problem=problem, difficulty='invalid_level'
            )

    def test_update_problem_should_change_difficulty(self, problem: Problem):
        ProblemService.update_problem(problem=problem, difficulty='hard')
        problem.refresh_from_db()
        assert problem.difficulty == 'hard'

    def test_deactivate_problem_should_set_is_active_false(
        self, problem: Problem
    ):
        assert problem.is_active is True
        ProblemService.deactivate_problem(problem)
        problem.refresh_from_db()
        assert problem.is_active is False

    def test_upsert_problem_should_create_new_record(self):
        title = 'Brand New Problem'

        problem, created = ProblemService.upsert_problem(
            title=title,
            description='New description',
            difficulty='easy',
            category='arrays',
            is_active=True,
        )

        assert created is True
        assert Problem.objects.filter(title=title).exists()
        assert problem.title == title
        assert problem.is_active is True

    def test_upsert_problem_should_update_existing_record(self, problem: Problem):
        new_description = 'Updated by upsert'

        updated_problem, created = ProblemService.upsert_problem(
            title=problem.title,
            description=new_description,
            difficulty=problem.difficulty,
            category=problem.category,
            is_active=False,
        )

        assert created is False
        assert updated_problem.id == problem.id

        problem.refresh_from_db()
        assert problem.description == new_description

