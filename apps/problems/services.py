from django.core.exceptions import ValidationError
from .models import Problem, DIFFICULTY_CHOICES

VALID_DIFFICULTY_KEYS = [choice[0] for choice in DIFFICULTY_CHOICES]


class ProblemService:
    def create_problem(
            self,
            title: str,
            description: str,
            difficulty: str,
            category: str
    ) -> Problem:
        if difficulty not in VALID_DIFFICULTY_KEYS:
            raise ValidationError('Invalid difficulty level')

        return Problem.objects.create(
            title=title,
            description=description,
            difficulty=difficulty,
            category=category,
        )

    def update_problem(
            self,
            problem: Problem,
            title: str | None = None,
            description: str | None = None,
            difficulty: str | None = None,
            category: str | None = None,
    ) -> Problem:
        if difficulty is not None and difficulty not in VALID_DIFFICULTY_KEYS:
            raise ValidationError('Invalid difficulty level')

        if title is not None:
            problem.title = title
        if description is not None:
            problem.description = description
        if difficulty is not None:
            problem.difficulty = difficulty
        if category is not None:
            problem.category = category

        problem.save()
        return problem

    def deactivate_problem(self, problem: Problem) -> Problem:
        problem.is_active = False
        problem.save()
        return problem
