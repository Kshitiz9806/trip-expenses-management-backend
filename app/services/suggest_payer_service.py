import uuid
from datetime import date

from app.core.enums import CategoryEnum
from app.core.exceptions import TripLimitsNotSetError, TripNotFoundError
from app.repositories.expense_repository import ExpenseRepository
from app.repositories.trip_limit_repository import TripLimitRepository
from app.repositories.trip_repository import TripRepository
from app.repositories.trip_user_repository import TripUserRepository
from app.services.dto import PayerCandidateResult, SuggestPayerResult


class SuggestPayerService:
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

    def suggest_payer(
        self, trip_id: uuid.UUID, category: CategoryEnum, day, amount: float | None = None
    ) -> SuggestPayerResult:
        if self.trip_repo.get_by_id(trip_id) is None:
            raise TripNotFoundError()

        limit_rows = self.trip_limit_repo.get_by_trip(trip_id)
        limit_row = next((row for row in limit_rows if row.category == category), None)
        if limit_row is None:
            raise TripLimitsNotSetError()
        daily_limit = limit_row.daily_limit_amount

        # Always evaluated against today — a suggestion for a backdated
        # expense doesn't make sense, since that money is already spent.
        today_expenses = self.expense_repo.list(trip_id, category=category, day=day)

        users = self.trip_user_repo.get_users_for_trip(trip_id)

        candidates: list[PayerCandidateResult] = []
        for user in users:
            spent_today = sum(e.amount for e in today_expenses if e.user_id == user.id)
            headroom = daily_limit - spent_today
            eligible = True if amount is None else headroom >= amount
            candidates.append(
                PayerCandidateResult(
                    user_id=user.id,
                    user_name=user.name,
                    headroom=headroom,
                    eligible=eligible,
                )
            )

        candidates.sort(key=lambda c: c.headroom, reverse=True)
        suggested = next((c for c in candidates if c.eligible), None)

        return SuggestPayerResult(
            suggested_user_id=suggested.user_id if suggested else None,
            candidates=candidates,
        )