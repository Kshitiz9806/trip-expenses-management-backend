import uuid
from datetime import date

from app.core.enums import CategoryEnum
from app.core.exceptions import (
    InvalidTripExpenseCategoryError,
    TripNotFoundError,
    UserNotFoundError,
)
from app.models.trip import Trip
from app.models.trip_limit import TripLimit
from app.models.trip_user import TripUser
from app.models.user import User
from app.repositories.trip_limit_repository import TripLimitRepository
from app.repositories.trip_repository import TripRepository
from app.repositories.trip_user_repository import TripUserRepository
from app.repositories.user_repository import UserRepository


class TripService:
    def __init__(
        self,
        trip_repo: TripRepository,
        trip_user_repo: TripUserRepository,
        trip_limit_repo: TripLimitRepository,
        user_repo: UserRepository,
    ):
        self.trip_repo = trip_repo
        self.trip_user_repo = trip_user_repo
        self.trip_limit_repo = trip_limit_repo
        self.user_repo = user_repo

    @staticmethod
    def _validate_limits(limits: list[tuple[CategoryEnum, float]]) -> None:
        categories = [category for category, _ in limits]
        if not categories or not set(categories).issubset(set(CategoryEnum)):
            raise InvalidTripExpenseCategoryError()
        if len(categories) != len(set(categories)):
            raise InvalidTripExpenseCategoryError()

    def create_trip(
        self,
        name: str,
        start_date: date,
        creator_user_id: uuid.UUID,
        limits: list[tuple[CategoryEnum, float]],
    ) -> Trip:
        # Creator must already exist (registered via POST /users first).
        if self.user_repo.get_by_id(creator_user_id) is None:
            raise UserNotFoundError()

        self._validate_limits(limits)
        limits_dict = dict(limits)
        trip_limits = [(category, limits_dict.get(category, 0.0)) for category in CategoryEnum]

        trip = self.trip_repo.create(name=name, start_date=start_date)
        self.trip_limit_repo.replace_all(trip.id, trip_limits)
        self.trip_user_repo.add(trip.id, creator_user_id)
        return trip

    def get_trip(self, trip_id: uuid.UUID) -> Trip:
        trip = self.trip_repo.get_by_id(trip_id)
        if trip is None:
            raise TripNotFoundError()
        return trip

    def join_trip(self, trip_id: uuid.UUID, user_id: uuid.UUID) -> TripUser:
        self.get_trip(trip_id)  # raises TripNotFoundError if missing
        if self.user_repo.get_by_id(user_id) is None:
            raise UserNotFoundError()
        return self.trip_user_repo.add(trip_id, user_id)

    def set_limits(
        self, trip_id: uuid.UUID, limits: list[tuple[CategoryEnum, float]]
    ) -> list[TripLimit]:
        self.get_trip(trip_id)  # raises TripNotFoundError if missing
        self._validate_limits(limits)
        return self.trip_limit_repo.replace_limit(trip_id, limits)

    def get_trip_users(self, trip_id: uuid.UUID) -> list[User]:
        self.get_trip(trip_id)  # raises TripNotFoundError if missing
        return self.trip_user_repo.get_users_for_trip(trip_id)

    def get_trip_limits(self, trip_id: uuid.UUID) -> list[TripLimit]:
        self.get_trip(trip_id)  # raises TripNotFoundError if missing
        return self.trip_limit_repo.get_by_trip(trip_id)

    def get_trips_for_user(self, user_id: uuid.UUID) -> list[Trip]:
        if self.user_repo.get_by_id(user_id) is None:
            raise UserNotFoundError()
        return self.trip_user_repo.get_trips_for_user(user_id)