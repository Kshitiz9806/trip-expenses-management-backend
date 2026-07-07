import uuid
from datetime import datetime, timezone

from sqlmodel import SQLModel, Field


class TripUser(SQLModel, table=True):
    __tablename__ = "trip_users"

    trip_id: uuid.UUID = Field(foreign_key="trips.id", primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", primary_key=True)
    joined_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))