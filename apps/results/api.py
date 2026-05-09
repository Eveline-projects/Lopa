from uuid import UUID
from ninja import Router
from ninja.errors import HttpError

from .models import Result
from .schemas import ResultSchema
from .services import ResultService

router = Router()


@router.get('results/{result_id}/', response=ResultSchema)
def get_result(request, result_id: UUID):
    try:
        return ResultService.get_result_by_id(result_id, user=request.user)
    except Result.DoesNotExist:
        raise HttpError(404, 'Result does not exist')


@router.get(
    'submissions/{submission_id}/results/', response=list[ResultSchema]
)
def get_results_for_submission(request, submission_id: UUID):
    return ResultService.get_results_for_submission(
        submission_id, request.user
    )
