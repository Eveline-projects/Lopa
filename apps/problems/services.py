import uuid
from django.core.exceptions import ValidationError
from apps.problems.exceptions import ProblemNotFound
from .models import Problem, DIFFICULTY_CHOICES
from .repositories import ProblemRepository

VALID_DIFFICULTY_KEYS = [choice[0] for choice in DIFFICULTY_CHOICES]


class ProblemService:
    @staticmethod
    def create_problem(
            title: str,
            description: str,
            difficulty: str,
            category: str
    ) -> Problem:
        if difficulty not in VALID_DIFFICULTY_KEYS:
            raise ValidationError('Invalid difficulty level')

        problem = Problem(
            title=title,
            description=description,
            difficulty=difficulty,
            category=category
        )

        return ProblemRepository.save(problem)

    @staticmethod
    def update_problem(
            problem: Problem,
            title: str | None = None,
            description: str | None = None,
            difficulty: str | None = None,
            category: str | None = None,
    ) -> Problem:
        if difficulty is not None and difficulty not in VALID_DIFFICULTY_KEYS:
            raise ValidationError('Invalid difficulty level')

        update_data = {}
        if title is not None:
            update_data['title'] = title
        if description is not None:
            update_data['description'] = description
        if difficulty is not None:
            update_data['difficulty'] = difficulty
        if category is not None:
            update_data['category'] = category

        return ProblemRepository.update(problem, **update_data)

    @staticmethod
    def deactivate_problem(problem: Problem) -> Problem:
        problem.is_active = False
        return ProblemRepository.save(problem)

    @staticmethod
    def get_all_problems():
        return ProblemRepository.list_active()

    @staticmethod
    def get_problem_by_id(problem_id: uuid.UUID) -> Problem:
        try:
            return ProblemRepository.get_active_by_id(problem_id)
        except Problem.DoesNotExist as exc:
            raise ProblemNotFound('Problem not found') from exc
