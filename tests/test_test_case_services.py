from django.core.exceptions import ValidationError
import pytest
from apps.problems import services
from apps.problems.models import TestCase as ProblemTestCase


@pytest.mark.django_db
class TestTestCaseService:
    def test_create_test_case_should_set_correct_fields(self, problem):
        test_case = services.create_test_case(
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
            services.create_test_case(
                problem=problem,
                input_data='',
                expected_output='4'
            )
        assert ProblemTestCase.objects.count() == initial_count

    def test_create_test_case_should_fail_on_empty_input(self, problem):
        with pytest.raises(ValidationError) as excinfo:
            services.create_test_case(
                problem=problem,
                input_data='  ',
                expected_output='4',
            )

        assert 'Input data cannot be empty' in str(excinfo.value)


    def test_create_test_case_should_fail_on_empty_expected_output(self, problem):
        with pytest.raises(ValidationError) as excinfo:
            services.create_test_case(
                problem=problem,
                input_data='2 + 2',
                expected_output='  ',
            )

        assert "Expected output cannot be empty" in str(excinfo.value)
