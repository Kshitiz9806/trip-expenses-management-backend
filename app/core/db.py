from sqlmodel import SQLModel, Session, create_engine

# SQLite file-based DB, sits at project root as trip_expense.db
DATABASE_URL = "sqlite:///./trip_expense.db"

# check_same_thread=False is required for SQLite when used with FastAPI's
# threaded request handling (multiple requests may use the same connection
# across threads). Safe here since we open a fresh Session per request.
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})


def init_db() -> None:
    """Create all tables. Import app.models first so metadata is populated."""
    import app.models  # noqa: F401  (ensures all table models are registered)

    SQLModel.metadata.create_all(engine)


def get_session():
    """FastAPI dependency — yields a DB session per request."""
    with Session(engine) as session:
        yield session