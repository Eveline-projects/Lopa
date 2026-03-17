import pytest
from django.contrib.auth.models import User
from apps.problems.models import Problem
from apps.engine.models import Submission


@pytest.fixture
def problem(db):
    return Problem.objects.create(
        description='description',
        title='Two Pointers',
        difficulty='easy',
        category='Strings',

    )


@pytest.fixture
def submission(db, problem):
    user = User.objects.create_user(
        username='Adam',
        email='adam@gmail.com',
        password='1234'
    )
    test_code = 'print("Hello World")'

    return Submission.objects.create(
        user=user,
        problem=problem,
        code=test_code,
        status='done'
    )
