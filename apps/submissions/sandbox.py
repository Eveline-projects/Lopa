import docker
import time
import requests
import logging
from django.conf import settings
from apps.results.models import Result


logger = logging.getLogger(__name__)

TIMEOUT_LIMIT = getattr(settings, 'SUBMISSION_TIMEOUT', 2.0)


def run_code_in_sandbox(temp_dir_path: str) -> tuple[str, float, str]:
    start_time = time.perf_counter()

    try:
        client = docker.from_env()

        # Run the container synchronously and wait for it to finish
        logs = client.containers.run(
            image='python:3.11-alpine',
            command="sh -c 'python /app/solution.py < /app/input.txt'",
            volumes={
                temp_dir_path: {
                    'bind': '/app',
                    'mode': 'ro',
                }  # 'ro' ensures user code cannot alter test files
            },
            timeout=TIMEOUT_LIMIT,
        )

        execution_time = time.perf_counter() - start_time
        actual_output = logs.decode('utf-8').strip()

        return actual_output, execution_time, Result.Status.PASSED

    except docker.errors.ContainerError as e:
        # Code exited with non-zero status (e.g., SyntaxError, ZeroDivisionError)
        execution_time = time.perf_counter() - start_time
        error_logs = e.stderr.decode('utf-8') if e.stderr else str(e)
        return error_logs.strip(), execution_time, Result.Status.RUNTIME_ERROR

    except requests.exceptions.Timeout as e:
        execution_time = time.perf_counter() - start_time
        logger.error('Sandbox has timeout: %s', e)
        return (
            'Time Limit Exceeded',
            execution_time,
            Result.Status.TIME_LIMIT_EXCEEDED,
        )

    except Exception as e:
        logger.error('Sandbox fatal error: %s', e)
        return str(e), 0.0, Result.Status.RUNTIME_ERROR
