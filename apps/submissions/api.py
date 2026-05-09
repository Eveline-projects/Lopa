from uuid import UUID
from ninja import Router, Status
from ninja.errors import HttpError
from django.core.exceptions import ValidationError

from apps.problems.exceptions import ProblemNotFound
from .models import Submission
from .schemas import SubmissionSchema, SubmissionCreateSchema
from .services import SubmissionService

router = Router()


@router.get('/submissions/{submission_id}/', response=SubmissionSchema)
def get_submission(request, submission_id: UUID):
    try:
        return SubmissionService.get_submission_by_id(submission_id)
    except Submission.DoesNotExist:
        raise HttpError(404, 'Submission not found')


@router.post(
    '/problems/{problem_id}/submissions/', response={201: SubmissionSchema}
)
def create_submission(request, problem_id: UUID, data: SubmissionCreateSchema):
    try:
        submission = SubmissionService.create_submission(
            user=request.user,
            problem_id=problem_id,
            code=data.code,
        )
        return Status(201, submission)
    except ProblemNotFound:
        raise HttpError(404, 'Problem not found')
    except ValidationError as e:
        raise HttpError(422, e.messages[0])


@router.get(
    '/problems/{problem_id}/submissions/', response=list[SubmissionSchema]
)
def get_submissions_for_problem(request, problem_id: UUID):
    return SubmissionService.get_submissions_for_problem(problem_id)
