from uuid import UUID
from ninja import Schema, Field
from pydantic import field_validator


class TestCaseSchema(Schema):
    id: UUID
    problem_id: UUID
    input_data: str
    expected_output: str
    is_hidden: bool


class TestCaseCreateSchema(Schema):
    problem_id: UUID
    input_data: str = Field(..., min_length=1)
    expected_output: str = Field(..., min_length=1)
    is_hidden: bool = False

    @field_validator('input_data', 'expected_output')
    @classmethod
    def not_empty_whitespace(cls, value: str) -> str:
        if not value.strip():
            raise ValueError(
                'Field cannot be empty or contain only whitespace.'
            )
        return value
