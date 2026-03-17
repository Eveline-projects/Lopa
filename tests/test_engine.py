import datetime

import pytest


@pytest.mark.django_db
def test_submission_user(submission):
    assert submission.user.username == 'Adam'


@pytest.mark.django_db
def test_submission_problem(submission, problem):
    assert submission.problem == problem


@pytest.mark.django_db
def test_submission_code(submission):
    assert submission.code == 'print("Hello World")'


@pytest.mark.django_db
def test_submission_status(submission):
    assert submission.status == 'done'


@pytest.mark.django_db
def test_submission_created_at(submission):
    assert isinstance(submission.created_at, datetime.datetime)
    assert submission.created_at is not None
