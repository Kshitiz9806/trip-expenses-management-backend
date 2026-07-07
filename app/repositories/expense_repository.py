import uuid
from datetime import date, datetime

from sqlmodel import Session, select, func

from app.core.enums import CategoryEnum, PaymentTypeEnum
from app.models.expense import Expense


class ExpenseRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(
        self,
        trip_id: uuid.UUID,
        user_id: uuid.UUID,
        category: CategoryEnum,
        payment_type: PaymentTypeEnum,
        amount: float,
        description: str | None = None,
        timestamp: datetime | None = None,
    ) -> Expense:
        # Only pass timestamp through if explicitly provided, so the model's
        # default_factory ("now") kicks in otherwise.
        kwargs = dict(
            trip_id=trip_id,
            user_id=user_id,
            category=category,
            payment_type=payment_type,
            amount=amount,
            description=description,
        )
        if timestamp is not None:
            kwargs["timestamp"] = timestamp

        expense = Expense(**kwargs)
        self.session.add(expense)
        self.session.commit()
        self.session.refresh(expense)
        return expense

    def list(
        self,
        trip_id: uuid.UUID,
        user_id: uuid.UUID | None = None,
        category: CategoryEnum | None = None,
        day: date | None = None,
    ) -> list[Expense]:
        statement = select(Expense).where(Expense.trip_id == trip_id)

        if user_id is not None:
            statement = statement.where(Expense.user_id == user_id)
        if category is not None:
            statement = statement.where(Expense.category == category)
        if day is not None:
            statement = statement.where(func.date(Expense.timestamp) == day.isoformat())

        statement = statement.order_by(Expense.timestamp.desc())
        return list(self.session.exec(statement).all())