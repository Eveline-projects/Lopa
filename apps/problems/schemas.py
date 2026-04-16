from uuid import UUID
from typing import Literal
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
