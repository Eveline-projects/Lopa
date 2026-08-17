from uuid import UUID

from django.db.models import QuerySet

from apps.problems.models import Problem


class ProblemRepository:
    @staticmethod
    def save(problem: Problem) -> Problem:
        problem.full_clean()
        problem.save()
        return problem

    @staticmethod
    def list_active() -> QuerySet[Problem]:
        return Problem.objects.filter(is_active=True)

    @staticmethod
    def get_by_id(problem_id: UUID) -> Problem | None:
        return Problem.objects.filter(id=problem_id).first()

    @staticmethod
    def get_active_by_id(problem_id: UUID) -> Problem | None:
        return Problem.objects.filter(id=problem_id, is_active=True).first()

    @staticmethod
    def update(problem: Problem, **fields) -> Problem:
        if not fields:
            return problem

        allowed_fields = {'title', 'description', 'difficulty', 'category'}

        for field, value in fields.items():
            if field not in allowed_fields:
                raise ValueError(
                    f'Field {field} is not allowed to be updated.'
                )
            # Apply only fields provided by the service layer.
            setattr(problem, field, value)

        return ProblemRepository.save(problem)

    @staticmethod
    def deactivate(problem: Problem) -> None:
        problem.is_active = False
        ProblemRepository.save(problem)

    @staticmethod
    def get_by_title(title: str) -> Problem | None:
        return Problem.objects.filter(title=title).first()
