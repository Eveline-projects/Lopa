from uuid import UUID
from ninja import Router
from django.core.exceptions import ValidationError
from ninja.errors import HttpError
from .models import Problem
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
    except Problem.DoesNotExist:
        raise HttpError(404, 'Problem not found')


@router.post('/', response=ProblemSchema)
def create_problem(request, data: ProblemCreateSchema):
    try:
        return ProblemService.create_problem(**data.model_dump())
    except ValidationError as e:
        raise HttpError(422, e.messages[0])
