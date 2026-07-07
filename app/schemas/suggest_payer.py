import uuid

from pydantic import BaseModel

from app.core.enums import CategoryEnum


class SuggestPayerRequest(BaseModel):
    category: CategoryEnum
    amount: float | None = None  # if provided, filters out users who'd bust their limit


class PayerCandidate(BaseModel):
    user_id: uuid.UUID
    user_name: str
    headroom: float
    eligible: bool


class SuggestPayerResponse(BaseModel):
    suggested_user_id: uuid.UUID | None  # null if no one is eligible
    candidates: list[PayerCandidate]  # full ranked list, for transparency/fallback UI