import pytest
from apps.problems.models import Problem
import uuid


@pytest.mark.django_db
def test_problem():
    problem = Problem.objects.create(
        description='description',
        title='Two Pointers',
        difficulty='easy',
        category='Strings',

    )
    assert problem.id is not None
    assert isinstance(problem.id, uuid.UUID)
    assert problem.description == 'description'
    assert problem.title == 'Two Pointers'
    assert problem.difficulty == 'EASY'
    assert problem.category == 'Strings'
