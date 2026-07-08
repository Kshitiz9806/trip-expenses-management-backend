from fastapi import APIRouter, Depends

from app.core.dependencies import get_user_service
from app.schemas.user import CreateUserRequest, UserResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=201)
def create_user(
    payload: CreateUserRequest,
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    user = user_service.create_user(payload.name)
    return UserResponse(id=user.id, name=user.name)
