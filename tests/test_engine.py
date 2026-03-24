import uuid

from apps.engine.models import Submission, Result


def test_submission_should_be_linked_to_correct_user(submission):
    assert submission.user.username == 'Adam'


def test_submission_should_be_linked_to_correct_problem(submission, problem):
    assert submission.problem == problem


def test_submission_should_store_submitted_code(submission):
    assert submission.code == 'print("Hello World")'


def test_submission_should_have_done_status_by_default(submission):
    assert Submission.objects.count() == 1
    assert submission.status == Submission.Status.DONE


def test_result_id_should_be_a_valid_uuid(result):
    assert isinstance(result.id, uuid.UUID)


def test_result_should_be_linked_to_correct_submission(result, submission):
    assert result.submission == submission


def test_result_should_be_linked_to_correct_test_case(result, test_case):
    assert result.test_case == test_case


def test_result_should_store_runtime_error_status(result):
    assert result.status == Result.Status.RUNTIME_ERROR


def test_result_should_store_actual_output_correctly(result):
    assert result.actual_output == '123'


def test_result_should_have_valid_execution_time(result):
    assert isinstance(result.execution_time, float)
    assert result.execution_time == 0.2


def test_submission_related_manager_should_access_results(submission, result):
    assert submission.results.count() == 1
    assert submission.results.first() == result


def test_result_string_representation(result):
    assert str(result) == result.actual_output
