import uuid

from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    name: str
    passkey: str


class UserResponse(BaseModel):
    id: uuid.UUID
    name: str
