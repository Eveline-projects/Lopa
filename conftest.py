import pytest
from apps.problems.models import Problem

@pytest.fixture
def problem(db):
    return Problem.objects.create(
        description='description',
        title='Two Pointers',
        difficulty='easy',
        category='Strings',

    )
