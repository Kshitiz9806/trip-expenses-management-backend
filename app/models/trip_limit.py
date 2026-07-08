import uuid

from sqlmodel import SQLModel, Field

from app.core.enums import CategoryEnum


class TripLimit(SQLModel, table=True):
    __tablename__ = "trip_limits"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    trip_id: uuid.UUID = Field(foreign_key="trips.id")
    category: CategoryEnum
    daily_limit_amount: float
