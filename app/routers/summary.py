import uuid
from datetime import date

from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_summary_service
from app.schemas.summary import CategorySpend, TripSummaryResponse, UserSummary
from app.services.summary_service import SummaryService

router = APIRouter(prefix="/trips", tags=["summary"])


@router.get("/{trip_id}/summary", response_model=TripSummaryResponse)
def get_summary(
    trip_id: uuid.UUID,
    day: date | None = Query(default=None),
    summary_service: SummaryService = Depends(get_summary_service),
) -> TripSummaryResponse:
    result = summary_service.get_summary(trip_id, day=day)
    return TripSummaryResponse(
        trip_id=result.trip_id,
        day=result.day,
        users=[
            UserSummary(
                user_id=user_result.user_id,
                user_name=user_result.user_name,
                by_category=[
                    CategorySpend(
                        category=cat.category,
                        spent=cat.spent,
                        daily_limit=cat.daily_limit,
                        limit=cat.limit,
                        remaining=cat.remaining,
                    )
                    for cat in user_result.by_category
                ],
                by_payment_type=user_result.by_payment_type,
                total_spent=user_result.total_spent,
            )
            for user_result in result.users
        ],
    )