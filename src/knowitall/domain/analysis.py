from enum import StrEnum
from typing import TypedDict
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator


class ScopeSource(StrEnum):
    USER_EXPLICIT = "USER_EXPLICIT"
    ENTITY_RESOLVED = "ENTITY_RESOLVED"
    SESSION_INHERITED = "SESSION_INHERITED"
    INFERRED = "INFERRED"
    UNRESOLVED = "UNRESOLVED"


class AnalysisIntent(StrEnum):
    KNOWLEDGE_SEARCH = "KNOWLEDGE_SEARCH"
    CHANGE_IMPACT = "CHANGE_IMPACT"
    REQUIREMENT_REVIEW = "REQUIREMENT_REVIEW"


class BusinessScope(BaseModel):
    business_line_ids: list[str] = Field(default_factory=list)
    source: ScopeSource = ScopeSource.UNRESOLVED
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    requires_confirmation: bool = False

    @model_validator(mode="after")
    def explicit_scope_must_have_labels(self) -> "BusinessScope":
        if self.source == ScopeSource.USER_EXPLICIT and not self.business_line_ids:
            raise ValueError("An explicit business scope must contain at least one label")
        return self


class AnalysisRequest(BaseModel):
    request_id: UUID = Field(default_factory=uuid4)
    conversation_id: UUID | None = None
    question: str = Field(min_length=1, max_length=10_000)
    business_line_ids: list[str] = Field(default_factory=list)


class AnalysisAnswer(BaseModel):
    request_id: UUID
    intent: AnalysisIntent
    effective_scope: BusinessScope
    conclusion: str
    evidence_ids: list[str] = Field(default_factory=list)
    uncertainty: list[str] = Field(default_factory=list)


class AnalysisState(TypedDict, total=False):
    request_id: str
    question: str
    requested_business_line_ids: list[str]
    effective_scope: dict[str, object]
    intent: str
    conclusion: str
    evidence_ids: list[str]
    uncertainty: list[str]
