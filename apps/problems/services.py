import uuid
from django.core.exceptions import ValidationError
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
            **kwargs
    ) -> Problem:
        difficulty = kwargs.get('difficulty')
        if difficulty and difficulty not in VALID_DIFFICULTY_KEYS:
            raise ValidationError('Invalid difficulty level')

        clean_fields = {field: value for field, value in kwargs.items() if value is not None}
        return ProblemRepository.update(problem, **clean_fields)

    @staticmethod
    def deactivate_problem(problem: Problem) -> Problem:
        problem.is_active = False
        return ProblemRepository.save(problem)

    @staticmethod
    def get_all_problems():
        return ProblemRepository.list_active()

    @staticmethod
    def get_problem_by_id(problem_id: uuid.UUID) -> Problem:
        return ProblemRepository.get_active_by_id(problem_id)
