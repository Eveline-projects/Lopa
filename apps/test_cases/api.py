from uuid import UUID
from ninja import Router, Status
from django.core.exceptions import ValidationError as DjangoValidationError
from ninja.errors import HttpError
from apps.problems.models import Problem
from .models import TestCase
from .schemas import TestCaseSchema, TestCaseCreateSchema
from .services import TestCaseService

router = Router()


@router.get('/test-cases/{test_case_id}/', response=TestCaseSchema)
def get_test_case(request, test_case_id: UUID):
    try:
        return TestCaseService.get_test_case_by_id(test_case_id)
    except TestCase.DoesNotExist:
        raise HttpError(404, 'Test case does not exist')


@router.post('/test-cases/', response={201: TestCaseSchema})
def create_test_case(request, data: TestCaseCreateSchema):
    try:
        problem = Problem.objects.get(id=data.problem_id)
        new_test_case = TestCaseService.create_test_case(
            problem=problem,
            input_data=data.input_data,
            expected_output=data.expected_output,
            is_hidden=data.is_hidden,
        )

        return Status(201, new_test_case)

    except Problem.DoesNotExist:
        raise HttpError(404, 'Problem not found')
    except DjangoValidationError as e:
        raise HttpError(400, e.messages[0])


@router.get('/problems/{problem_id}/test-cases/', response=list[TestCaseSchema])
def get_test_cases_for_problem(request, problem_id: UUID):
    return TestCaseService.get_test_cases_for_problem(problem_id)
