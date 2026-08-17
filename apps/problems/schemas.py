from typing import Literal
from uuid import UUID

from ninja import Schema


class ProblemSchema(Schema):
    id: UUID
    title: str
    description: str
    difficulty: Literal['easy', 'medium', 'hard']
    category: str
    is_active: bool


class ProblemCreateSchema(Schema):
    title: str
    description: str
    difficulty: Literal['easy', 'medium', 'hard']
    category: str


class ProblemUpdateSchema(Schema):
    title: str | None = None
    description: str | None = None
    difficulty: Literal['easy', 'medium', 'hard'] | None = None
    category: str | None = None
