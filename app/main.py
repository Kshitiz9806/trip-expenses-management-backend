from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.db import init_db
from app.core.exceptions import (
    DomainException,
    InvalidTripExpenseCategoryError,
    TripLimitsNotSetError,
    TripNotFoundError,
    UserNotFoundError,
    UserNotInTripError,
)
from app.routers import expenses, suggest_payer, summary, trips, users

# Maps each domain exception to its HTTP status code. A single handler below
# (registered on the DomainException base class) catches every subclass via
# Starlette's MRO-based exception lookup, so this table is the only place
# status codes need to be maintained.
EXCEPTION_STATUS_MAP: dict[type[DomainException], int] = {
    TripNotFoundError: 404,
    UserNotFoundError: 404,
    TripLimitsNotSetError: 409,
    UserNotInTripError: 403,
    InvalidTripExpenseCategoryError: 400,
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Trip Expense Tracker API", lifespan=lifespan)


@app.exception_handler(DomainException)
def domain_exception_handler(request: Request, exc: DomainException) -> JSONResponse:
    status_code = EXCEPTION_STATUS_MAP.get(type(exc), 400)
    return JSONResponse(status_code=status_code, content={"detail": exc.message})


app.include_router(users.router)
app.include_router(trips.router)
app.include_router(expenses.router)
app.include_router(summary.router)
app.include_router(suggest_payer.router)
