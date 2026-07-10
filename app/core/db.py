import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, Session, create_engine

load_dotenv()

# Reads DATABASE_URL from the environment (set this on Render to your Neon
# Postgres connection string). Falls back to a local SQLite file when
# unset, so local dev is unaffected.
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    DATABASE_URL = "sqlite:///./trip_expense.db"

# Neon/Render/Heroku-style providers hand out "postgres://" URLs, but
# SQLAlchemy 1.4+/2.0 requires the "postgresql://" scheme.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# check_same_thread=False is required for SQLite when used with FastAPI's
# threaded request handling (multiple requests may use the same connection
# across threads). Safe here since we open a fresh Session per request.

# check_same_thread=False is only relevant/needed for SQLite; Postgres
# doesn't use this connect arg at all.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)


def init_db() -> None:
    """Create all tables. Import app.models first so metadata is populated."""
    import app.models  # noqa: F401  (ensures all table models are registered)

    SQLModel.metadata.create_all(engine)


def get_session():
    """FastAPI dependency — yields a DB session per request."""
    with Session(engine) as session:
        yield session
