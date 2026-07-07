import uuid
from datetime import date

from sqlmodel import Session

from app.models.trip import Trip


class TripRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, name: str, start_date: date) -> Trip:
        trip = Trip(name=name, start_date=start_date)
        self.session.add(trip)
        self.session.commit()
        self.session.refresh(trip)
        return trip

    def get_by_id(self, trip_id: uuid.UUID) -> Trip | None:
        return self.session.get(Trip, trip_id)