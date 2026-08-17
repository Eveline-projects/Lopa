import os

import pytest
from playwright.sync_api import Page

from apps.problems.models import Problem
from apps.test_cases.models import TestCase

os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'


@pytest.fixture(autouse=True)
def enable_celery_eager_mode(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True


@pytest.fixture
def e2e_page(page: Page, live_server, user):

    user.set_password('testpass123')
    user.save()

    page.goto(f'{live_server.url}/login/')

    page.fill('input[name="username"]', user.username)
    page.fill('input[name="password"]', 'testpass123')
    page.get_by_role('button').click()

    page.wait_for_load_state('networkidle')

    return page


@pytest.fixture
def problem(db):
    p = Problem.objects.create(
        description='description',
        title='Two Pointers',
        difficulty='easy',
        category='Strings',
    )
    TestCase.objects.create(
        problem=p,
        input_data='[1,2,3]',
        expected_output='[0,1]',
        is_hidden=False,
    )
    return p
