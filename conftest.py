import pytest
from django.contrib.auth.models import User
from apps.problems.models import Problem, TestCase
from apps.engine.models import Submission
from apps.problems.models import Problem
from apps.engine.models import Submission, Result


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='Adam',
        email='adam@gmail.com',
        password='testpassword123'
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
        status=Submission.Status.DONE,
    )

@pytest.fixture
def result(db, submission, test_case):
    return Result.objects.create(
        submission=submission,
        test_case=test_case,
        status=Result.Status.RUNTIME_ERROR,
        actual_output='123',
        execution_time=0.2,
    )
