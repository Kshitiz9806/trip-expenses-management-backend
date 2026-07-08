from fastapi import Depends
from sqlmodel import Session

from app.core.db import get_session
from app.repositories.expense_repository import ExpenseRepository
from app.repositories.trip_limit_repository import TripLimitRepository
from app.repositories.trip_repository import TripRepository
from app.repositories.trip_user_repository import TripUserRepository
from app.repositories.user_repository import UserRepository
from app.services.expense_service import ExpenseService
from app.services.suggest_payer_service import SuggestPayerService
from app.services.summary_service import SummaryService
from app.services.trip_service import TripService
from app.services.user_service import UserService

# --- Repositories ---
# Each takes the same per-request Session (FastAPI caches Depends results
# within a single request), so all repository writes in one request share
# a transaction.


def get_user_repository(session: Session = Depends(get_session)) -> UserRepository:
    return UserRepository(session)


def get_trip_repository(session: Session = Depends(get_session)) -> TripRepository:
    return TripRepository(session)


def get_trip_user_repository(
    session: Session = Depends(get_session),
) -> TripUserRepository:
    return TripUserRepository(session)


def get_trip_limit_repository(
    session: Session = Depends(get_session),
) -> TripLimitRepository:
    return TripLimitRepository(session)


def get_expense_repository(
    session: Session = Depends(get_session),
) -> ExpenseRepository:
    return ExpenseRepository(session)


# --- Services ---


def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repo)


def get_trip_service(
    trip_repo: TripRepository = Depends(get_trip_repository),
    trip_user_repo: TripUserRepository = Depends(get_trip_user_repository),
    trip_limit_repo: TripLimitRepository = Depends(get_trip_limit_repository),
    user_repo: UserRepository = Depends(get_user_repository),
) -> TripService:
    return TripService(trip_repo, trip_user_repo, trip_limit_repo, user_repo)


def get_expense_service(
    expense_repo: ExpenseRepository = Depends(get_expense_repository),
    trip_repo: TripRepository = Depends(get_trip_repository),
    trip_user_repo: TripUserRepository = Depends(get_trip_user_repository),
    user_repo: UserRepository = Depends(get_user_repository),
) -> ExpenseService:
    return ExpenseService(expense_repo, trip_repo, trip_user_repo, user_repo)


def get_summary_service(
    expense_repo: ExpenseRepository = Depends(get_expense_repository),
    trip_repo: TripRepository = Depends(get_trip_repository),
    trip_user_repo: TripUserRepository = Depends(get_trip_user_repository),
    trip_limit_repo: TripLimitRepository = Depends(get_trip_limit_repository),
) -> SummaryService:
    return SummaryService(expense_repo, trip_repo, trip_user_repo, trip_limit_repo)


def get_suggest_payer_service(
    expense_repo: ExpenseRepository = Depends(get_expense_repository),
    trip_repo: TripRepository = Depends(get_trip_repository),
    trip_user_repo: TripUserRepository = Depends(get_trip_user_repository),
    trip_limit_repo: TripLimitRepository = Depends(get_trip_limit_repository),
) -> SuggestPayerService:
    return SuggestPayerService(expense_repo, trip_repo, trip_user_repo, trip_limit_repo)
