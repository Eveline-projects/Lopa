import logging
from uuid import UUID

from ninja import Router
from ninja.errors import HttpError

from .models import Result
from .schemas import ResultSchema
from .services import ResultService

logger = logging.getLogger(__name__)

router = Router()


@router.get('results/{result_id}/', response=ResultSchema)
def get_result(request, result_id: UUID):
    logger.info('get_result request id=%s', result_id)
    try:
        return ResultService.get_result_by_id(result_id, user=request.user)
    except Result.DoesNotExist:
        logger.warning('result not found id=%s', result_id)
        raise HttpError(404, 'Result does not exist')


@router.get(
    'submissions/{submission_id}/results/', response=list[ResultSchema]
)
def get_results_for_submission(request, submission_id: UUID):
    logger.info(
        'get_results_for_submission request submission_id=%s', submission_id
    )
    return ResultService.get_results_for_submission(
        submission_id, request.user
    )
