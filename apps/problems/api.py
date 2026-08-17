import logging
from uuid import UUID

from django.core.exceptions import ValidationError
from ninja import Router, Status
from ninja.errors import HttpError

from apps.problems.exceptions import ProblemNotFound

from .schemas import ProblemCreateSchema, ProblemSchema, ProblemUpdateSchema
from .services import ProblemService

logger = logging.getLogger(__name__)

router = Router()


@router.get('/', response=list[ProblemSchema])
def list_problems(request):
    logger.info('list_problems request')
    return ProblemService.get_all_problems()


@router.get('/{problem_id}/', response=ProblemSchema)
def get_problem(request, problem_id: UUID):
    logger.info('get_problem request id=%s', problem_id)
    try:
        return ProblemService.get_problem_by_id(problem_id)
    except ProblemNotFound:
        raise HttpError(404, 'Problem not found')


@router.post('/', response={201: ProblemSchema})
def create_problem(request, data: ProblemCreateSchema):
    logger.info('create_problem request')
    try:
        new_problem = ProblemService.create_problem(**data.model_dump())
        return Status(201, new_problem)
    except ValidationError as e:
        logger.warning(
            'create_problem validation failed error=%s', e.messages[0]
        )
        raise HttpError(422, e.messages[0])


@router.patch('/{problem_id}/', response=ProblemSchema)
def update_problem(request, problem_id: UUID, data: ProblemUpdateSchema):
    logger.info('update_problem request id=%s', problem_id)
    try:
        problem = ProblemService.get_problem_for_update_or_delete(problem_id)
        updated_problem = ProblemService.update_problem(
            problem, **data.model_dump(exclude_unset=True)
        )
        return updated_problem
    except ProblemNotFound:
        raise HttpError(404, 'Problem not found')
    except ValidationError as e:
        logger.warning(
            'update_problem validation failed id=%s error=%s',
            problem_id,
            e.messages[0],
        )
        raise HttpError(422, e.messages[0])


@router.delete('/{problem_id}/', response={204: None})
def delete_problem(request, problem_id: UUID):
    logger.info('delete_problem request id=%s', problem_id)
    try:
        problem = ProblemService.get_problem_for_update_or_delete(problem_id)
        ProblemService.deactivate_problem(problem)
        return Status(204, None)
    except ProblemNotFound:
        raise HttpError(404, 'Problem not found')
