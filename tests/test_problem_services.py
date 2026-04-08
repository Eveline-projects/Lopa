from django.core.exceptions import ValidationError
import pytest
from apps.problems import services
from apps.problems.models import Problem


@pytest.mark.django_db
class TestProblemService:
    def test_create_problem_should_set_correct_fields(self):
        new_problem = services.create_problem(
            title='Easy Problem',
            description='Test',
            difficulty='easy',
            category='Test'
        )
        assert new_problem.title == 'Easy Problem'
        assert new_problem.description == 'Test'
        assert new_problem.difficulty == 'easy'
        assert new_problem.category == 'Test'
        assert new_problem.is_active is True

    def test_create_problem_should_create_record_in_db(self):
        new_problem = services.create_problem(
            title='Easy Problem',
            description='Test',
            difficulty='easy',
            category='Test'
        )
        assert Problem.objects.count() == 1
        assert new_problem.title == 'Easy Problem'

    def test_create_problem_should_raise_error_on_invalid_difficulty(self):
        with pytest.raises(ValidationError):
            services.create_problem(
                title='Test',
                description='Test',
                difficulty='invalid_level',
                category='Test'
            )

    def test_update_problem_should_update_only_provided_fields(self, problem: Problem):
        old_difficulty = problem.difficulty
        new_title = 'New Title'

        services.update_problem(problem, title=new_title)

        problem.refresh_from_db()
        assert problem.title == new_title
        assert problem.difficulty == old_difficulty

    def test_update_problem_should_raise_error_on_invalid_difficulty(self, problem: Problem):
        with pytest.raises(ValidationError):
            services.update_problem(
                problem,
                difficulty="invalid_level"
            )

    def test_update_problem_should_change_difficulty(self, problem: Problem):
        services.update_problem(
            problem,
            difficulty='hard'
        )
        problem.refresh_from_db()
        assert problem.difficulty == 'hard'

    def test_delete_problem_should_deactivate_problem(self, problem: Problem):
        services.deactivate_problem(problem)
        problem.refresh_from_db()
        assert problem.is_active is False
