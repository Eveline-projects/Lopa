import logging
import time

import docker
import requests
from django.conf import settings

from apps.results.models import Result

logger = logging.getLogger(__name__)


def run_code_in_sandbox(
    code_content: str, input_data: str = ''
) -> tuple[str, float, str]:
    timeout_limit = getattr(settings, 'SUBMISSION_TIMEOUT', 5.0)
    client = docker.from_env()
    start_time = time.perf_counter()
    container = None

    cmd = f'echo {input_data!r} | python -c {code_content!r}'

    try:
        # Configure bomb protection and memory limits
        ulimits = [{'Name': 'nproc', 'Soft': 50, 'Hard': 50}]

        # Run the container synchronously and wait for it to finish
        container = client.containers.run(
            image='python:3.13-alpine',
            command=['sh', '-c', cmd],
            network_mode='none',
            mem_limit='128m',
            nano_cpus=1000000000,
            pids_limit=64,
            ulimits=ulimits,
            detach=True,
        )

        try:
            result_status = container.wait(timeout=timeout_limit)
            exit_code = result_status.get('StatusCode', 0)
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout,
        ):
            try:
                container.kill()
            except docker.errors.APIError:
                logger.warning('Failed to kill container during timeout cleanup')
            execution_time = time.perf_counter() - start_time
            return (
                'Time Limit Exceeded',
                execution_time,
                Result.Status.TIME_LIMIT_EXCEEDED,
            )

        execution_time = time.perf_counter() - start_time
        raw_logs = container.logs(stdout=True, stderr=True)
        max_bytes = 10 * 1024
        actual_output = (
            raw_logs[:max_bytes].decode('utf-8', errors='replace').strip()
        )

        if exit_code != 0:
            return (
                actual_output if actual_output else 'Runtime Error',
                execution_time,
                Result.Status.RUNTIME_ERROR,
            )

        return actual_output, execution_time, Result.Status.PASSED

    except docker.errors.DockerException as e:
        execution_time = time.perf_counter() - start_time
        logger.exception('Sandbox fatal error')
        return str(e), execution_time, Result.Status.RUNTIME_ERROR

    finally:
        if container:
            try:
                container.remove(force=True)
            except docker.errors.APIError as e:
                logger.warning('Failed to remove container during cleanup: %s', e)
