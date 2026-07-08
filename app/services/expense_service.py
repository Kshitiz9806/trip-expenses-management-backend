import uuid
from datetime import date, datetime

from app.core.enums import CategoryEnum, PaymentTypeEnum
from app.core.exceptions import TripNotFoundError, UserNotFoundError, UserNotInTripError
from app.models.expense import Expense
from app.repositories.expense_repository import ExpenseRepository
from app.repositories.trip_repository import TripRepository
from app.repositories.trip_user_repository import TripUserRepository
from app.repositories.user_repository import UserRepository


class ExpenseService:
    def __init__(
        self,
        expense_repo: ExpenseRepository,
        trip_repo: TripRepository,
        trip_user_repo: TripUserRepository,
        user_repo: UserRepository,
    ):
        self.expense_repo = expense_repo
        self.trip_repo = trip_repo
        self.trip_user_repo = trip_user_repo
        self.user_repo = user_repo

    def _ensure_trip_exists(self, trip_id: uuid.UUID) -> None:
        if self.trip_repo.get_by_id(trip_id) is None:
            raise TripNotFoundError()

    def add_expense(
        self,
        trip_id: uuid.UUID,
        user_id: uuid.UUID,
        category: CategoryEnum,
        payment_type: PaymentTypeEnum,
        amount: float,
        description: str | None = None,
        timestamp: datetime | None = None,
    ) -> Expense:
        self._ensure_trip_exists(trip_id)

        if self.user_repo.get_by_id(user_id) is None:
            raise UserNotFoundError()

        if not self.trip_user_repo.is_member(trip_id, user_id):
            raise UserNotInTripError()

        return self.expense_repo.create(
            trip_id=trip_id,
            user_id=user_id,
            category=category,
            payment_type=payment_type,
            amount=amount,
            description=description,
            timestamp=timestamp,
        )

    def list_expenses(
        self,
        trip_id: uuid.UUID,
        user_id: uuid.UUID | None = None,
        category: CategoryEnum | None = None,
        day: date | None = None,
    ) -> list[Expense]:
        self._ensure_trip_exists(trip_id)
        return self.expense_repo.list(
            trip_id, user_id=user_id, category=category, day=day
        )
