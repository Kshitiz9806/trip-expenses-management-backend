import uuid

from app.core.exceptions import UserNotFoundError
from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def login_or_register(self, name: str, passkey: str) -> User:
        existing = self.user_repo.get_by_name_and_passkey(name, passkey)
        if existing is not None:
            return existing
        return self.user_repo.create(name=name, passkey=passkey)

    def get_user(self, user_id: uuid.UUID) -> User:
        user = self.user_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError()
        return user
