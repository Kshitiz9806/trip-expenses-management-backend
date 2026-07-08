import uuid

from fastapi import APIRouter, Depends

from app.core.dependencies import get_trip_service
from app.schemas.trip import (
    CreateTripRequest,
    SetTripLimitsRequest,
    TripLimitInput,
    TripLimitsResponse,
    TripResponse,
    TripSummaryItem,
    TripUserResponse,
    UserTripsResponse,
)
from app.schemas.user import UserResponse
from app.services.trip_service import TripService

router = APIRouter(prefix="/trips", tags=["trips"])


def _build_trip_response(trip_service: TripService, trip_id: uuid.UUID) -> TripResponse:
    trip = trip_service.get_trip(trip_id)
    limits = trip_service.get_trip_limits(trip_id)
    users = trip_service.get_trip_users(trip_id)
    return TripResponse(
        id=trip.id,
        name=trip.name,
        start_date=trip.start_date,
        created_at=trip.created_at,
        limits=[
            TripLimitInput(
                category=limit.category, daily_limit_amount=limit.daily_limit_amount
            )
            for limit in limits
        ],
        users=[UserResponse(id=user.id, name=user.name) for user in users],
    )


@router.get("", response_model=UserTripsResponse)
def list_trips_for_user(
    user_id: uuid.UUID,
    trip_service: TripService = Depends(get_trip_service),
) -> UserTripsResponse:
    """Returns the trips a given user has joined, for the frontend's home
    screen (trip picker). Returns lightweight items only — call
    GET /trips/{trip_id} for full detail once a trip is selected."""
    trips = trip_service.get_trips_for_user(user_id)
    return UserTripsResponse(
        trips=[
            TripSummaryItem(id=t.id, name=t.name, start_date=t.start_date)
            for t in trips
        ]
    )


@router.post("", response_model=TripResponse, status_code=201)
def create_trip(
    payload: CreateTripRequest,
    trip_service: TripService = Depends(get_trip_service),
) -> TripResponse:
    limits = [(limit.category, limit.daily_limit_amount) for limit in payload.limits]
    trip = trip_service.create_trip(
        name=payload.name,
        start_date=payload.start_date,
        creator_user_id=payload.creator_user_id,
        limits=limits,
    )
    return _build_trip_response(trip_service, trip.id)


@router.get("/{trip_id}", response_model=TripResponse)
def get_trip(
    trip_id: uuid.UUID,
    trip_service: TripService = Depends(get_trip_service),
) -> TripResponse:
    return _build_trip_response(trip_service, trip_id)


@router.put("/{trip_id}/users/{user_id}", response_model=TripUserResponse)
def join_trip(
    trip_id: uuid.UUID,
    user_id: uuid.UUID,
    trip_service: TripService = Depends(get_trip_service),
) -> TripUserResponse:
    trip_user = trip_service.join_trip(trip_id, user_id)
    return TripUserResponse(
        trip_id=trip_user.trip_id,
        user_id=trip_user.user_id,
        joined_at=trip_user.joined_at,
    )


@router.put("/{trip_id}/limits", response_model=TripLimitsResponse)
def set_trip_limits(
    trip_id: uuid.UUID,
    payload: SetTripLimitsRequest,
    trip_service: TripService = Depends(get_trip_service),
) -> TripLimitsResponse:
    limits = [(limit.category, limit.daily_limit_amount) for limit in payload.limits]
    updated = trip_service.set_limits(trip_id, limits)
    return TripLimitsResponse(
        trip_id=trip_id,
        limits=[
            TripLimitInput(
                category=limit.category, daily_limit_amount=limit.daily_limit_amount
            )
            for limit in updated
        ],
    )
