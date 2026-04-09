from django.core.exceptions import ValidationError
from .models import Problem, DIFFICULTY_CHOICES, TestCase

VALID_DIFFICULTY_KEYS = [choice[0] for choice in DIFFICULTY_CHOICES]


def create_problem(title: str, description: str, difficulty: str, category: str) -> Problem:
    if difficulty not in VALID_DIFFICULTY_KEYS:
        raise ValidationError('Invalid difficulty level')

    return Problem.objects.create(
        title=title,
        description=description,
        difficulty=difficulty,
        category=category,
    )


def update_problem(
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


def deactivate_problem(problem: Problem) -> Problem:
    problem.is_active = False
    problem.save()
    return problem


def create_test_case(problem: Problem, input_data: str, expected_output: str, is_hidden: bool = False) -> TestCase:
    if not input_data.strip():
        raise ValidationError('Input data cannot be empty')
    if not expected_output.strip():
        raise ValidationError('Expected output cannot be empty')

    return TestCase.objects.create(
        problem=problem,
        input_data=input_data,
        expected_output=expected_output,
        is_hidden=is_hidden,
    )
