import uuid
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel, UniqueConstraint


class User(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("name", "passkey", name="uq_user_name_passkey"),)

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    passkey: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
