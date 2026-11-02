from typing import Literal
from pydantic import BaseModel, Field, field_validator

class AnalysisRequest(BaseModel):
    statement_a: str = Field(min_length=1, max_length=2000)
    statement_b: str = Field(min_length=1, max_length=2000)

    @field_validator("statement_a", "statement_b")
    @classmethod
    def validate_statements(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Statement cannot be empty or whitespace.")
        return value

class AnalysisResponse(BaseModel):
    classification: Literal[
        "direct_contradiction",
        "partial_conflict",
        "compatible",
        "insufficient_information"
    ]

    explanation: str
    evidence: list[str]
    possible_explanations: list[str]

    confidence: Literal["low", "medium", "high"]