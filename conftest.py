import pytest

from apps.problems.models import Problem
from apps.results.models import Result
from apps.submissions.models import Submission
from apps.test_cases.models import TestCase
from apps.users.models import User


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='Adam',
        email='adam@gmail.com',
        password='testpassword123',
    )


@pytest.fixture
def problem(db):
    return Problem.objects.create(
        description='description',
        title='Two Pointers',
        difficulty='easy',
        category='Strings',
    )


@pytest.fixture
def test_case(db, problem):
    return TestCase.objects.create(
        problem=problem,
        input_data='[1,2,3]',
        expected_output='[0,1]',
        is_hidden=False,
    )


@pytest.fixture
def submission(db, user, problem):
    return Submission.objects.create(
        user=user,
        problem=problem,
        code='print("Hello World")',
    )


@pytest.fixture
def result(db, submission, test_case):
    return Result.objects.create(
        submission=submission,
        test_case=test_case,
        actual_output='123',
        execution_time=0.2,
    )


@pytest.fixture
def other_result(db, user, problem, test_case):
    other_submission = Submission.objects.create(
        user=user,
        problem=problem,
        code='print(2)',
    )
    return Result.objects.create(
        submission=other_submission,
        test_case=test_case,
        status=Result.Status.WRONG_ANSWER,
        actual_output='wrong answer',
        execution_time=0.02,
    )
