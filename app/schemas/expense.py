import uuid
from datetime import datetime

from pydantic import BaseModel

from app.core.enums import CategoryEnum, PaymentTypeEnum


class CreateExpenseRequest(BaseModel):
    user_id: uuid.UUID  # who paid
    category: CategoryEnum
    payment_type: PaymentTypeEnum
    amount: float
    description: str | None = None
    # Optional — omit for "now" (default), or provide for a backdated entry.
    timestamp: datetime | None = None


class ExpenseResponse(BaseModel):
    id: uuid.UUID
    trip_id: uuid.UUID
    user_id: uuid.UUID
    category: CategoryEnum
    payment_type: PaymentTypeEnum
    amount: float
    description: str | None
    timestamp: datetime


class ExpenseListResponse(BaseModel):
    expenses: list[ExpenseResponse]
