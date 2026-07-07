import uuid
from datetime import date

from pydantic import BaseModel

from app.core.enums import CategoryEnum, PaymentTypeEnum


class CategorySpend(BaseModel):
    category: CategoryEnum
    spent: float
    daily_limit: float
    limit: float
    remaining: float


class UserSummary(BaseModel):
    user_id: uuid.UUID
    user_name: str
    by_category: list[CategorySpend]
    by_payment_type: dict[PaymentTypeEnum, float]
    total_spent: float


class TripSummaryResponse(BaseModel):
    trip_id: uuid.UUID
    day: date | None  # echoes back the filter used; null = all-time
    users: list[UserSummary]