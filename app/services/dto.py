import uuid
from dataclasses import dataclass, field
from datetime import date

from app.core.enums import CategoryEnum, PaymentTypeEnum


@dataclass
class CategorySpendResult:
    category: CategoryEnum
    spent: float
    daily_limit: float
    limit: float  # daily_limit for day-filtered queries; daily_limit * days_elapsed for all-time
    remaining: float


@dataclass
class UserSummaryResult:
    user_id: uuid.UUID
    user_name: str
    by_category: list[CategorySpendResult]
    by_payment_type: dict[PaymentTypeEnum, float]
    total_spent: float


@dataclass
class TripSummaryResult:
    trip_id: uuid.UUID
    day: date | None
    users: list[UserSummaryResult] = field(default_factory=list)


@dataclass
class PayerCandidateResult:
    user_id: uuid.UUID
    user_name: str
    headroom: float
    eligible: bool


@dataclass
class SuggestPayerResult:
    suggested_user_id: uuid.UUID | None
    candidates: list[PayerCandidateResult] = field(default_factory=list)
