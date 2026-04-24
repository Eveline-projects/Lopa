from uuid import UUID
from typing import Literal
from ninja import Schema


class ResultSchema(Schema):
    id: UUID
    submission_id: UUID
    test_case_id: UUID
    status: Literal[
        'PENDING',
        'PASSED',
        'WRONG_ANSWER',
        'TIME_LIMIT_EXCEEDED',
        'RUNTIME_ERROR',
    ]
    actual_output: str | None = None
    execution_time: float | None = None
