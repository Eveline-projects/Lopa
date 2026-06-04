import pytest
import docker
import requests
from unittest.mock import patch
from apps.results.models import Result
from apps.submissions.sandbox import run_code_in_sandbox


@pytest.mark.django_db
@patch('apps.submissions.sandbox.client.containers.run')
class TestRunCodeInSandbox:
    def test_run_code_in_sandbox_should_return_passed_on_success(
        self, mock_docker_run
    ):
        mock_docker_run.return_value = b'Hello World\n'

        output, exec_time, status = run_code_in_sandbox('/tmp/fake_dir')

        assert status == Result.Status.PASSED
        assert output == 'Hello World'
        assert isinstance(exec_time, float)
        assert exec_time >= 0.0

    def test_run_code_in_sandbox_should_return_runtime_error_on_container_crash(
        self, mock_docker_run
    ):
        container_exception = docker.errors.ContainerError(
            container=None,
            exit_status=1,
            command='python solution.py',
            image='python:3.11-alpine',
            stderr=b'ZeroDivisionError: division by zero\n',
        )
        mock_docker_run.side_effect = container_exception

        output, exec_time, status = run_code_in_sandbox('/tmp/fake_dir')

        assert status == Result.Status.RUNTIME_ERROR
        assert 'ZeroDivisionError' in output
        assert isinstance(exec_time, float)

    def test_run_code_in_sandbox_should_return_time_limit_exceeded_on_timeout(
        self, mock_docker_run
    ):
        mock_docker_run.side_effect = requests.exceptions.Timeout(
            'Container timed out'
        )

        output, exec_time, status = run_code_in_sandbox('/tmp/fake_dir')

        assert status == Result.Status.TIME_LIMIT_EXCEEDED
        assert output == 'Time Limit Exceeded'
        assert isinstance(exec_time, float)

    def test_run_code_in_sandbox_should_return_runtime_error_on_fatal_system_exception(
        self, mock_docker_run
    ):
        mock_docker_run.side_effect = Exception(
            'Docker daemon connection lost'
        )

        output, exec_time, status = run_code_in_sandbox('/tmp/fake_dir')

        assert status == Result.Status.RUNTIME_ERROR
        assert 'Docker daemon connection lost' in output
        assert exec_time == 0.0
