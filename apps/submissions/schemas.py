from datetime import datetime
from typing import Literal
from uuid import UUID

from ninja import Schema


class SubmissionSchema(Schema):
    id: UUID
    user_id: int
    problem_id: UUID
    code: str
    created_at: datetime
    status: Literal['PENDING', 'DONE', 'WRONG_ANSWER', 'ERROR']


class SubmissionCreateSchema(Schema):
    code: str
