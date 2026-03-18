import pytest
from django.contrib.auth.models import User
from apps.problems.models import Problem
from apps.engine.models import Submission


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
def submission(db, user, problem):
    return Submission.objects.create(
        user=user,
        problem=problem,
        code='print("Hello World")',
        status=Submission.Status.DONE,
    )
