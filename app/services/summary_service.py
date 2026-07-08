import uuid
from datetime import date

from app.core.enums import CategoryEnum, PaymentTypeEnum
from app.core.exceptions import TripLimitsNotSetError, TripNotFoundError
from app.repositories.expense_repository import ExpenseRepository
from app.repositories.trip_limit_repository import TripLimitRepository
from app.repositories.trip_repository import TripRepository
from app.repositories.trip_user_repository import TripUserRepository
from app.services.dto import CategorySpendResult, TripSummaryResult, UserSummaryResult


class SummaryService:
    def __init__(
        self,
        expense_repo: ExpenseRepository,
        trip_repo: TripRepository,
        trip_user_repo: TripUserRepository,
        trip_limit_repo: TripLimitRepository,
    ):
        self.expense_repo = expense_repo
        self.trip_repo = trip_repo
        self.trip_user_repo = trip_user_repo
        self.trip_limit_repo = trip_limit_repo

    def get_summary(
        self, trip_id: uuid.UUID, day: date | None = None
    ) -> TripSummaryResult:
        trip = self.trip_repo.get_by_id(trip_id)
        if trip is None:
            raise TripNotFoundError()

        limit_rows = self.trip_limit_repo.get_by_trip(trip_id)
        if not limit_rows:
            raise TripLimitsNotSetError()
        daily_limits: dict[CategoryEnum, float] = {
            row.category: row.daily_limit_amount for row in limit_rows
        }

        # Day-filtered: compare against a single day's limit.
        # All-time: compare cumulative spend against limit * days elapsed so far,
        # since limits are a per-day allowance, not a trip-wide total.
        if day is not None:
            limit_multiplier = 1
            expenses = self.expense_repo.list(trip_id, day=day)
        else:
            days_elapsed = (date.today() - trip.start_date).days + 1
            limit_multiplier = max(days_elapsed, 1)
            expenses = self.expense_repo.list(trip_id)

        users = self.trip_user_repo.get_users_for_trip(trip_id)

        user_summaries: list[UserSummaryResult] = []
        for user in users:
            user_expenses = [e for e in expenses if e.user_id == user.id]

            by_category: list[CategorySpendResult] = []
            for category in CategoryEnum:
                spent = sum(e.amount for e in user_expenses if e.category == category)
                daily_limit = daily_limits.get(category, 0.0)
                limit = daily_limit * limit_multiplier
                by_category.append(
                    CategorySpendResult(
                        category=category,
                        spent=spent,
                        daily_limit=daily_limit,
                        limit=limit,
                        remaining=limit - spent,
                    )
                )

            by_payment_type: dict[PaymentTypeEnum, float] = {}
            for payment_type in PaymentTypeEnum:
                total = sum(
                    e.amount for e in user_expenses if e.payment_type == payment_type
                )
                if total:
                    by_payment_type[payment_type] = total

            user_summaries.append(
                UserSummaryResult(
                    user_id=user.id,
                    user_name=user.name,
                    by_category=by_category,
                    by_payment_type=by_payment_type,
                    total_spent=sum(e.amount for e in user_expenses),
                )
            )

        return TripSummaryResult(trip_id=trip_id, day=day, users=user_summaries)
