import pytest
import uuid


@pytest.mark.django_db
class TestTestCaseService:
    def test_test_cases_id_should_be_a_valid_uuid(self, test_case):
        assert isinstance(test_case.id, uuid.UUID)

    def test_test_cases_should_be_linked_to_correct_problem(
        self, test_case, problem
    ):
        assert test_case.problem == problem

    def test_test_cases_should_store_input_data_correctly(self, test_case):
        assert test_case.input_data == '[1,2,3]'

    def test_test_cases_should_store_expected_output_correctly(
        self, test_case
    ):
        assert test_case.expected_output == '[0,1]'

    def test_test_cases_is_visible_by_default(self, test_case):
        assert test_case.is_hidden is False

    def test_problem_related_manager_should_return_all_associated_test_cases(
        self, problem, test_case
    ):
        assert problem.test_cases.count() == 1
        assert problem.test_cases.first() == test_case

    def test_test_cases_string_representation(self, test_case):
        assert str(test_case) == f'Test for {test_case.problem.title}'
