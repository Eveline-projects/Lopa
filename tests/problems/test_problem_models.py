import uuid

import pytest


@pytest.mark.django_db
class TestProblemModel:
    def test_problem_id_should_be_a_valid_uuid(self, problem):
        assert problem.id is not None
        assert isinstance(problem.id, uuid.UUID)

    def test_problem_should_store_correct_title(self, problem):
        assert problem.title == 'Two Pointers'

    def test_problem_should_store_correct_description(self, problem):
        assert problem.description == 'description'

    def test_problem_should_have_assigned_difficulty_level(self, problem):
        assert problem.difficulty == 'easy'

    def test_problem_should_belong_to_correct_category(self, problem):
        assert problem.category == 'Strings'
