from apps.engine.models import Submission


def test_submission_user(submission):
    assert submission.user.username == 'Adam'


def test_submission_problem(submission, problem):
    assert submission.problem == problem


def test_submission_code(submission):
    assert submission.code == 'print("Hello World")'


def test_submission_status(submission):
    assert Submission.objects.count() == 1
    assert submission.status == Submission.Status.DONE
