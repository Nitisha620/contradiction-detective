from typing import Literal
from pydantic import BaseModel, Field


class AnalysisRequest(BaseModel):
    statement_a: str = Field(min_length=1, max_length=2000)
    statement_b: str = Field(min_length=1, max_length=2000)


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