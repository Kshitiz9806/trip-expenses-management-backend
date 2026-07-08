import uuid

from sqlmodel import Session, select

from app.models.trip import Trip
from app.models.trip_user import TripUser
from app.models.user import User


class TripUserRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, trip_id: uuid.UUID, user_id: uuid.UUID) -> TripUser:
        """Idempotent join: if the user is already a member, return the
        existing row instead of creating a duplicate."""
        existing = self.session.get(TripUser, (trip_id, user_id))
        if existing:
            return existing

        trip_user = TripUser(trip_id=trip_id, user_id=user_id)
        self.session.add(trip_user)
        self.session.commit()
        self.session.refresh(trip_user)
        return trip_user

    def is_member(self, trip_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        return self.session.get(TripUser, (trip_id, user_id)) is not None

    def get_users_for_trip(self, trip_id: uuid.UUID) -> list[User]:
        statement = (
            select(User)
            .join(TripUser, TripUser.user_id == User.id)
            .where(TripUser.trip_id == trip_id)
        )
        return list(self.session.exec(statement).all())

    def get_trips_for_user(self, user_id: uuid.UUID) -> list[Trip]:
        statement = (
            select(Trip)
            .join(TripUser, TripUser.trip_id == Trip.id)
            .where(TripUser.user_id == user_id)
        )
        return list(self.session.exec(statement).all())
