import uuid
import pytest
from apps.test_cases.models import TestCase
from apps.test_cases.repositories import TestCaseRepository

@pytest.mark.django_db
class TestTestCaseRepository:
    def test_create_returns_saved_test_case(self, problem):
        test_case = TestCaseRepository.create(
            problem=problem,
            input_data='[1,2,3]',
            expected_output='[0,1]',
            is_hidden=False,
        )

        assert test_case.id is not None
        assert test_case.problem == problem
        assert test_case.input_data == '[1,2,3]'
        assert TestCase.objects.count() == 1

    def test_get_test_cases_for_problem_returns_all_test_cases(self, problem):
        TestCase.objects.create(
            problem=problem,
            input_data='in1',
            expected_output='out1',
        )
        TestCase.objects.create(
            problem=problem,
            input_data='in2',
            expected_output='out2',
        )

        queryset = TestCaseRepository.get_test_cases_for_problem(problem.id)
        assert queryset.count() == 2
        input_data = {tc.input_data for tc in queryset}
        assert input_data == {'in1', 'in2'}

    def test_get_by_id_returns_test_case(self, problem):
        created = TestCase.objects.create(
            problem=problem,
            input_data='in',
            expected_output='out',
        )

        test_case = TestCaseRepository.get_by_id(created.id)
        assert test_case == created

    def test_get_by_id_raises_does_not_exist(self):
        with pytest.raises(TestCase.DoesNotExist):
            TestCaseRepository.get_by_id(uuid.uuid4())