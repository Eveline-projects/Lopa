import uuid
from apps.problems.models import Problem


class ProblemRepository:
    @staticmethod
    def save(problem: Problem) -> Problem:
        problem.full_clean()
        problem.save()
        return problem

    @staticmethod
    def create(title, description, difficulty, category) -> Problem:
        problem = Problem(
            title=title,
            description=description,
            difficulty=difficulty,
            category=category,
        )
        return ProblemRepository.save(problem)

    @staticmethod
    def list_active():
        return Problem.objects.filter(is_active=True)

    @staticmethod
    def get_active_by_id(problem_id: uuid.UUID):
        return Problem.objects.get(id=problem_id, is_active=True)

    @staticmethod
    def update(problem: Problem, **fields) -> Problem:
        for field, value in fields.items():
            # Apply only fields provided by the service layer.
            setattr(problem, field, value)
        return ProblemRepository.save(problem)
