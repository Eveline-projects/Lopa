from uuid import UUID
from django.db.models import QuerySet
from django.core.exceptions import ValidationError
from apps.problems.exceptions import ProblemNotFound
from .models import Problem, DIFFICULTY_CHOICES
from .repositories import ProblemRepository

VALID_DIFFICULTY_KEYS = {choice[0] for choice in DIFFICULTY_CHOICES}


class ProblemService:
    @staticmethod
    def create_problem(
        title: str, description: str, difficulty: str, category: str
    ) -> Problem:
        if difficulty not in VALID_DIFFICULTY_KEYS:
            raise ValidationError('Invalid difficulty level')

        problem = Problem(
            title=title,
            description=description,
            difficulty=difficulty,
            category=category,
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
    def deactivate_problem(problem: Problem) -> None:
        ProblemRepository.deactivate(problem)

    @staticmethod
    def get_all_problems() -> QuerySet[Problem]:
        return ProblemRepository.list_active()

    @staticmethod
    def get_problem_by_id(problem_id: UUID) -> Problem:
        problem = ProblemRepository.get_active_by_id(problem_id)
        if not problem:
            raise ProblemNotFound('Problem not found')

        return problem

    @staticmethod
    def get_problem_for_update_or_delete(problem_id: UUID) -> Problem:
        problem = ProblemRepository.get_by_id(problem_id)
        if not problem:
            raise ProblemNotFound('Problem not found')

        return problem

    @staticmethod
    def seed_problem(
        title: str,
        description: str,
        difficulty: str,
        category: str,
        is_active: bool = True,
    ) -> tuple[Problem, bool]:
        existing_problem = ProblemRepository.get_by_title(title)

        if existing_problem:
            updated = ProblemService.update_problem(
                problem=existing_problem,
                description=description,
                difficulty=difficulty,
                category=category,
            )
            if is_active and not updated.is_active:
                updated.is_active = True
                ProblemRepository.save(updated)

            return updated, False
        new_problem = Problem.Service.create_problem(
            title=title,
            description=description,
            difficulty=difficulty,
            category=category,
        )
        return new_problem, True
