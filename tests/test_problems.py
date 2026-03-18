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
