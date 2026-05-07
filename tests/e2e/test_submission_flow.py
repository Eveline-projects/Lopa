import pytest
from playwright.sync_api import expect


@pytest.mark.django_db(transaction=True)
class TestSubmissionFlow:
    def test_successful_submission_shows_results(
        self, e2e_page, live_server, problem
    ):
        e2e_page.goto(f'{live_server.url}/problems/{problem.id}/')

        expected = problem.test_cases.first().expected_output
        e2e_page.fill('#code-input', expected)
        e2e_page.click('#submit-btn')

        results_container = e2e_page.locator('#results-table-body')
        expect(results_container).to_contain_text('PASSED', timeout=20000)

    def test_different_statuses(self, e2e_page, live_server, problem):
        e2e_page.goto(f'{live_server.url}/problems/{problem.id}/')

        e2e_page.fill('#code-input', 'wrong')
        e2e_page.click('#submit-btn')

        results_container = e2e_page.locator('#results-table-body')
        expect(results_container).to_contain_text(
            'WRONG_ANSWER', timeout=20000
        )
