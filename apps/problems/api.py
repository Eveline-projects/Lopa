from uuid import UUID
from ninja import Router, Status
from django.core.exceptions import ValidationError
from ninja.errors import HttpError
from .models import Problem
from .schemas import ProblemSchema, ProblemCreateSchema, ProblemUpdateSchema
from apps.problems.exceptions import ProblemNotFound
from .schemas import ProblemSchema, ProblemCreateSchema
from .services import ProblemService

router = Router()


@router.get('/', response=list[ProblemSchema])
def list_problems(request):
    return ProblemService.get_all_problems()


@router.get('/{problem_id}/', response=ProblemSchema)
def get_problem(request, problem_id: UUID):
    try:
        return ProblemService.get_problem_by_id(problem_id)
    except ProblemNotFound:
        raise HttpError(404, 'Problem not found')


@router.post('/', response={201: ProblemSchema})
def create_problem(request, data: ProblemCreateSchema):
    try:
        new_problem = ProblemService.create_problem(**data.model_dump())
        return Status(201, new_problem)
    except ValidationError as e:
        raise HttpError(422, e.messages[0])


@router.patch('/{problem_id}/', response=ProblemSchema)
def update_problem(request, problem_id: UUID, data: ProblemUpdateSchema):
    try:
        problem = ProblemService.get_problem_by_id(problem_id)
        updated_problem = ProblemService.update_problem(
            problem,
            **data.model_dump(exclude_unset=True)
        )
        return updated_problem
    except Problem.DoesNotExist:
        raise HttpError(404, 'Problem not found')

@router.delete('/{problem_id}/', response={204: None})
def delete_problem(request, problem_id: UUID):
    try:
        ProblemService.deactivate_problem(problem_id)
        return Status(204, None)
    except Problem.DoesNotExist:
        raise HttpError(404, 'Problem not found')
