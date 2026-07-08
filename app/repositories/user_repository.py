import uuid

from sqlmodel import Session, select

from app.models.user import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, name: str) -> User:
        user = User(name=name)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return self.session.get(User, user_id)

    def get_by_ids(self, user_ids: list[uuid.UUID]) -> list[User]:
        if not user_ids:
            return []
        statement = select(User).where(User.id.in_(user_ids))
        return list(self.session.exec(statement).all())
