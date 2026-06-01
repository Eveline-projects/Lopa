import logging
from uuid import UUID
from ninja import Router, Status
from ninja.errors import HttpError
from django.core.exceptions import ValidationError

from apps.problems.exceptions import ProblemNotFound
from .models import Submission
from .schemas import SubmissionSchema, SubmissionCreateSchema
from .services import SubmissionService
from apps.submissions.services import SubmissionEvaluationService

logger = logging.getLogger(__name__)

router = Router()


@router.get('/submissions/{submission_id}/', response=SubmissionSchema)
def get_submission(request, submission_id: UUID):
    logger.info('get_submission request id=%s', submission_id)
    try:
        return SubmissionService.get_submission_by_id(submission_id)
    except Submission.DoesNotExist:
        raise HttpError(404, 'Submission not found')


@router.post(
    '/problems/{problem_id}/submissions/', response={201: SubmissionSchema}
)
def create_submission(request, problem_id: UUID, data: SubmissionCreateSchema):
    user_id = getattr(request.user, 'id', None)
    logger.info(
        'create_submission request problem_id=%s user_id=%s code_size=%d',
        problem_id,
        user_id,
        len(data.code) if data.code else 0,
    )

    try:
        submission = SubmissionService.create_submission(
            user=request.user,
            problem_id=problem_id,
            code=data.code,
        )
        try:
            SubmissionEvaluationService.evaluate(submission)
        except Exception as eval_err:
            logger.error(
                'Evaluation engine failed for submission_id=%s, but submission was successfully saved to DB.',
                submission.id,
                exc_info=True,
            )

        return Status(201, submission)

    except ProblemNotFound:
        raise HttpError(404, 'Problem not found')
    except ValidationError as e:
        logger.warning(
            'create_submission validation failed problem_id=%s error=%s',
            problem_id,
            e.messages[0],
        )
        raise HttpError(422, e.messages[0])


@router.get(
    '/problems/{problem_id}/submissions/', response=list[SubmissionSchema]
)
def get_submissions_for_problem(request, problem_id: UUID):
    logger.info(
        'get_submissions_for_problem request problem_id=%s', problem_id
    )
    return SubmissionService.get_submissions_for_problem(problem_id)
