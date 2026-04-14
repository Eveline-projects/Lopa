from django.core.exceptions import ValidationError
import pytest
from apps.test_cases.services import TestCaseService
from apps.test_cases.models import TestCase as ProblemTestCase
from apps.problems.models import Problem


@pytest.mark.django_db
class TestTestCaseService:
    def test_create_test_case_should_set_correct_fields(self, problem):
        test_case = TestCaseService.create_test_case(
            problem=problem,
            input_data='2 + 2',
            expected_output='4',
            is_hidden=True
        )

        assert ProblemTestCase.objects.count() == 1
        assert test_case.problem == problem
        assert test_case.input_data == '2 + 2'
        assert test_case.expected_output == '4'
        assert test_case.is_hidden is True

    def test_create_test_case_should_not_save_to_db_on_validation_error(self, problem):
        initial_count = ProblemTestCase.objects.count()

        with pytest.raises(ValidationError):
            TestCaseService.create_test_case(
                problem=problem,
                input_data='',
                expected_output='4'
            )
        assert ProblemTestCase.objects.count() == initial_count

    def test_create_test_case_should_fail_on_empty_input(self, problem):
        with pytest.raises(ValidationError) as excinfo:
            TestCaseService.create_test_case(
                problem=problem,
                input_data='  ',
                expected_output='4',
            )

        assert 'Input data cannot be empty' in str(excinfo.value)

    def test_create_test_case_should_fail_on_empty_expected_output(self, problem):
        with pytest.raises(ValidationError) as excinfo:
            TestCaseService.create_test_case(
                problem=problem,
                input_data='2 + 2',
                expected_output='  ',
            )

        assert "Expected output cannot be empty" in str(excinfo.value)

    def test_get_test_cases_for_problem_should_return_only_test_cases_for_selected_problem(
            self,
            problem
    ):
        other_problem = Problem.objects.create(
            title='Other problem',
            description='Other description',
            difficulty='easy',
            category='arrays',
        )
        first_test_case = ProblemTestCase.objects.create(
            problem=problem,
            input_data='1 2',
            expected_output='3',
        )
        second_test_case = ProblemTestCase.objects.create(
            problem=problem,
            input_data='2 2',
            expected_output='4',
        )
        ProblemTestCase.objects.create(
            problem=other_problem,
            input_data='5 5',
            expected_output='10',
        )

        result = TestCaseService.get_test_cases_for_problem(problem.id)
        assert result.count() == 2
        assert first_test_case in result
        assert second_test_case in result
        assert all(test_case.problem_id == problem.id for test_case in result)

    def test_get_test_case_by_id_should_return_test_case(self, problem):
        test_case = ProblemTestCase.objects.create(
            problem=problem,
            input_data='10 20',
            expected_output='30',
        )

        result = TestCaseService.get_test_case_by_id(test_case.id)

        assert result == test_case
        assert result.problem == problem
        assert result.input_data == '10 20'
        assert result.expected_output == '30'

    def test_get_test_case_by_id_should_raise_error_for_nonexistent_id(self):
        with pytest.raises(ProblemTestCase.DoesNotExist):
            TestCaseService.get_test_case_by_id(999999)
