import pytest
from unittest.mock import patch
from playwright.sync_api import expect
from apps.results.models import Result


@pytest.mark.django_db(transaction=True)
class TestSubmissionFlow:
    def test_successful_submission_shows_results(
        self, e2e_page, live_server, problem
    ):
        e2e_page.goto(f'{live_server.url}/problems/{problem.id}/')

        expected = problem.test_cases.first().expected_output

        with patch(
            'apps.submissions.status_services.run_code_in_sandbox'
        ) as mock_sandbox:
            mock_sandbox.return_value = (expected, 0.1, Result.Status.PASSED)
            e2e_page.fill('#code-input', f'print("""{expected}""")')
            e2e_page.click('#submit-btn')

            results_container = e2e_page.locator('#results-table-body')
            expect(results_container).to_contain_text('PASSED', timeout=20000)

    def test_different_statuses(self, e2e_page, live_server, problem):
        e2e_page.goto(f'{live_server.url}/problems/{problem.id}/')

        with patch(
            'apps.submissions.status_services.run_code_in_sandbox'
        ) as mock_sandbox:
            mock_sandbox.return_value = (
                'Completely wrong result',
                0.1,
                # Mocking PASSED with incorrect output to force a WRONG_ANSWER status for testing
                Result.Status.PASSED,
            )

            e2e_page.fill('#code-input', 'print("Completely wrong result")')
            e2e_page.click('#submit-btn')

            results_container = e2e_page.locator('#results-table-body')
            expect(results_container).to_contain_text(
                'WRONG_ANSWER', timeout=20000
            )
