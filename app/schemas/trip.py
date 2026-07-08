import uuid
from datetime import date, datetime

from pydantic import BaseModel

from app.core.enums import CategoryEnum
from app.schemas.user import UserResponse


class TripLimitInput(BaseModel):
    category: CategoryEnum
    daily_limit_amount: float


class CreateTripRequest(BaseModel):
    name: str
    start_date: date
    creator_user_id: uuid.UUID
    limits: list[TripLimitInput]  # must contain exactly one entry per category


class TripResponse(BaseModel):
    id: uuid.UUID
    name: str
    start_date: date
    created_at: datetime
    limits: list[TripLimitInput]
    users: list[UserResponse]


class SetTripLimitsRequest(BaseModel):
    limits: list[TripLimitInput]  # replaces all existing limits for the trip


class TripLimitsResponse(BaseModel):
    trip_id: uuid.UUID
    limits: list[TripLimitInput]


class TripUserResponse(BaseModel):
    trip_id: uuid.UUID
    user_id: uuid.UUID
    joined_at: datetime

class TripSummaryItem(BaseModel):
    id: uuid.UUID
    name: str
    start_date: date

class UserTripsResponse(BaseModel):
    trips: list[TripSummaryItem]