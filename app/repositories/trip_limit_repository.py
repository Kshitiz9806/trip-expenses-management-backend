import uuid

from sqlmodel import Session, select

from app.core.enums import CategoryEnum
from app.models.trip_limit import TripLimit


class TripLimitRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_trip(self, trip_id: uuid.UUID) -> list[TripLimit]:
        statement = select(TripLimit).where(TripLimit.trip_id == trip_id)
        return list(self.session.exec(statement).all())

    def replace_limit(
        self, trip_id: uuid.UUID, limits: list[tuple[CategoryEnum, float]]
    ) -> list[TripLimit]:
        existing_limits = self.get_by_trip(trip_id)
        existing_by_category = {row.category: row for row in self.get_by_trip(trip_id)}
        for category, amount in limits:
            existing_row = existing_by_category.get(category)
            if existing_row is not None:
                self.session.delete(existing_row)
            self.session.add(TripLimit(trip_id=trip_id, category=category, daily_limit_amount=amount))
        self.session.commit()
        return self.get_by_trip(trip_id=trip_id)
        

    def replace_all(
        self, trip_id: uuid.UUID, limits: list[tuple[CategoryEnum, float]]
    ) -> list[TripLimit]:
        """Idempotent replace: delete any existing limits for this trip and
        insert the new set, in one transaction."""
        existing = self.get_by_trip(trip_id)
        for row in existing:
            self.session.delete(row)

        new_rows = [
            TripLimit(trip_id=trip_id, category=category, daily_limit_amount=amount)
            for category, amount in limits
        ]
        for row in new_rows:
            self.session.add(row)

        self.session.commit()
        for row in new_rows:
            self.session.refresh(row)
        return new_rows