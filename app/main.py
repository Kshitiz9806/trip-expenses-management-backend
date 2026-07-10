from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
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

import os
from dotenv import load_dotenv

load_dotenv()

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

FRONTEND_URL = os.getenv("FRONTEND_API_URL")

# Dev-time CORS: allows the Vite dev server (localhost and LAN IP, since
# you're testing from a phone on the same network) to call this API.
# allow_origins=["*"] is fine here since there's no auth/cookies involved
# (allow_credentials must be False when using a wildcard origin).
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(DomainException)
def domain_exception_handler(request: Request, exc: DomainException) -> JSONResponse:
    status_code = EXCEPTION_STATUS_MAP.get(type(exc), 400)
    return JSONResponse(status_code=status_code, content={"detail": exc.message})


app.include_router(users.router)
app.include_router(trips.router)
app.include_router(expenses.router)
app.include_router(summary.router)
app.include_router(suggest_payer.router)
