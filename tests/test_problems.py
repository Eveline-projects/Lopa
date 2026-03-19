import uuid


def test_problem_id_should_be_a_valid_uuid(problem):
    assert problem.id is not None
    assert isinstance(problem.id, uuid.UUID)


def test_problem_should_store_correct_title(problem):
    assert problem.title == 'Two Pointers'


def test_problem_should_store_correct_description(problem):
    assert problem.description == 'description'


def test_problem_should_have_assigned_difficulty_level(problem):
    assert problem.difficulty == 'easy'


def test_problem_should_belong_to_correct_category(problem):
    assert problem.category == 'Strings'


def test_test_case_id_should_be_a_valid_uuid(test_case):
    assert isinstance(test_case.id, uuid.UUID)


def test_test_case_should_be_linked_to_correct_problem(test_case, problem):
    assert test_case.problem == problem


def test_test_case_should_store_input_data_correctly(test_case):
    assert test_case.input_data == '[1,2,3]'


def test_test_case_should_store_expected_output_correctly(test_case):
    assert test_case.expected_output == '[0,1]'


def test_test_case_is_visible_by_default(test_case):
    assert test_case.is_hidden is False


def test_problem_related_manager_should_return_all_associated_test_cases(problem, test_case):
    assert problem.testcases.count() == 1
    assert problem.testcases.first() == test_case


def test_test_case_string_representation(test_case):
    assert str(test_case) == f"Test for {test_case.problem.title}"
