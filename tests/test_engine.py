from apps.engine.models import Submission


def test_submission_should_be_linked_to_correct_user(submission):
    assert submission.user.username == 'Adam'


def test_submission_should_be_linked_to_correct_problem(submission, problem):
    assert submission.problem == problem


def test_submission_should_store_submitted_code(submission):
    assert submission.code == 'print("Hello World")'


def test_submission_should_have_done_status_by_default(submission):
    assert Submission.objects.count() == 1
    assert submission.status == Submission.Status.DONE
