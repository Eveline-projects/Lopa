import uuid
import pytest


@pytest.mark.django_db
def test_problem_id_is_uuid(problem):
    assert problem.id is not None
    assert isinstance(problem.id, uuid.UUID)


@pytest.mark.django_db
def test_problem_title(problem):
    assert problem.title == 'Two Pointers'


@pytest.mark.django_db
def test_problem_description(problem):
    assert problem.description == 'description'


@pytest.mark.django_db
def test_problem_stores_difficulty(problem):
    assert problem.difficulty == 'easy'


@pytest.mark.django_db
def test_problem_category(problem):
    assert problem.category == 'Strings'
