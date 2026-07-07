import uuid
from datetime import datetime, timezone

from sqlmodel import SQLModel, Field

from app.core.enums import CategoryEnum, PaymentTypeEnum


class Expense(SQLModel, table=True):
    __tablename__ = "expenses"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    trip_id: uuid.UUID = Field(foreign_key="trips.id")
    user_id: uuid.UUID = Field(foreign_key="users.id")  # who paid
    category: CategoryEnum
    payment_type: PaymentTypeEnum
    amount: float
    description: str | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))