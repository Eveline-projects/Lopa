import uuid


def test_problem_id_is_uuid(problem):
    assert problem.id is not None
    assert isinstance(problem.id, uuid.UUID)


def test_problem_title(problem):
    assert problem.title == 'Two Pointers'


def test_problem_description(problem):
    assert problem.description == 'description'


def test_problem_stores_difficulty(problem):
    assert problem.difficulty == 'easy'


def test_problem_category(problem):
    assert problem.category == 'Strings'


def test_test_case_id_is_uuid(test_case):
    assert isinstance(test_case.id, uuid.UUID)


def test_test_case_problem(test_case, problem):
    assert test_case.problem == problem


def test_test_case_input_data(test_case):
    assert test_case.input_data == '[1,2,3]'


def test_test_case_expected_output(test_case):
    assert test_case.expected_output == '[0,1]'


def test_test_case_is_hidden(test_case):
    assert test_case.is_hidden


def test_problem_can_access_test_case(problem, test_case):
    assert problem.testcases.count() == 1
    assert problem.testcases.first() == test_case
