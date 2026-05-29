import logging
from uuid import UUID
from django.db.models import QuerySet
from django.core.exceptions import ValidationError
from apps.problems.exceptions import ProblemNotFound
from .models import Problem, DIFFICULTY_CHOICES
from .repositories import ProblemRepository

logger = logging.getLogger(__name__)

VALID_DIFFICULTY_KEYS = {choice[0] for choice in DIFFICULTY_CHOICES}


class ProblemService:
    @staticmethod
    def create_problem(
        title: str,
        description: str,
        difficulty: str,
        category: str,
        is_active: bool = True,
    ) -> Problem:
        if difficulty not in VALID_DIFFICULTY_KEYS:
            logger.warning(
                'Problem creation failed: invalid difficulty=%s', difficulty
            )
            raise ValidationError('Invalid difficulty level')

        problem = Problem(
            title=title,
            description=description,
            difficulty=difficulty,
            category=category,
            is_active=is_active,
        )

        saved = ProblemRepository.save(problem)
        logger.info(
            'problem created id=%s title=%s difficulty=%s',
            saved.id,
            saved.title,
            saved.difficulty,
        )
        return saved

    @staticmethod
    def update_problem(
        problem: Problem,
        title: str | None = None,
        description: str | None = None,
        difficulty: str | None = None,
        category: str | None = None,
    ) -> Problem:
        if difficulty is not None and difficulty not in VALID_DIFFICULTY_KEYS:
            logger.warning(
                'Problem update failed: invalid difficulty=%s id%s',
                difficulty,
                problem.id,
            )
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

        updated = ProblemRepository.update(problem, **update_data)
        logger.info(
            'problem updated id=%s fields=%s',
            updated.id,
            list(update_data),
        )
        return updated

    @staticmethod
    def deactivate_problem(problem: Problem) -> None:
        ProblemRepository.deactivate(problem)
        logger.info('problem deactivated id=%s', problem.id)

    @staticmethod
    def get_all_problems() -> QuerySet[Problem]:
        return ProblemRepository.list_active()

    @staticmethod
    def get_problem_by_id(problem_id: UUID) -> Problem:
        problem = ProblemRepository.get_active_by_id(problem_id)
        if not problem:
            logger.warning('problem not found id=%s', problem_id)
            raise ProblemNotFound('Problem not found')

        return problem

    @staticmethod
    def get_problem_for_update_or_delete(problem_id: UUID) -> Problem:
        problem = ProblemRepository.get_by_id(problem_id)
        if not problem:
            logger.warning('problem not found id=%s', problem_id)
            raise ProblemNotFound('Problem not found')

        return problem

    @staticmethod
    def upsert_problem(
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
            return updated, False

        new_problem = ProblemService.create_problem(
            title=title,
            description=description,
            difficulty=difficulty,
            category=category,
            is_active=is_active,
        )
        return new_problem, True
