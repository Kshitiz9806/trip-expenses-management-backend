import uuid

from fastapi import APIRouter, Depends

from app.core.dependencies import get_suggest_payer_service
from app.schemas.suggest_payer import PayerCandidate, SuggestPayerRequest, SuggestPayerResponse
from app.services.suggest_payer_service import SuggestPayerService

router = APIRouter(prefix="/trips", tags=["suggest-payer"])


@router.post("/{trip_id}/suggest-payer", response_model=SuggestPayerResponse)
def suggest_payer(
    trip_id: uuid.UUID,
    payload: SuggestPayerRequest,
    service: SuggestPayerService = Depends(get_suggest_payer_service),
) -> SuggestPayerResponse:
    result = service.suggest_payer(trip_id, category=payload.category, amount=payload.amount)
    return SuggestPayerResponse(
        suggested_user_id=result.suggested_user_id,
        candidates=[
            PayerCandidate(
                user_id=c.user_id,
                user_name=c.user_name,
                headroom=c.headroom,
                eligible=c.eligible,
            )
            for c in result.candidates
        ],
    )