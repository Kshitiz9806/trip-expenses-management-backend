import uuid
from datetime import date

from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_expense_service
from app.core.enums import CategoryEnum
from app.schemas.expense import CreateExpenseRequest, ExpenseListResponse, ExpenseResponse
from app.services.expense_service import ExpenseService

router = APIRouter(prefix="/trips", tags=["expenses"])


def _to_expense_response(expense) -> ExpenseResponse:
    return ExpenseResponse(
        id=expense.id,
        trip_id=expense.trip_id,
        user_id=expense.user_id,
        category=expense.category,
        payment_type=expense.payment_type,
        amount=expense.amount,
        description=expense.description,
        timestamp=expense.timestamp,
    )


@router.post("/{trip_id}/expenses", response_model=ExpenseResponse, status_code=201)
def add_expense(
    trip_id: uuid.UUID,
    payload: CreateExpenseRequest,
    expense_service: ExpenseService = Depends(get_expense_service),
) -> ExpenseResponse:
    expense = expense_service.add_expense(
        trip_id=trip_id,
        user_id=payload.user_id,
        category=payload.category,
        payment_type=payload.payment_type,
        amount=payload.amount,
        description=payload.description,
        timestamp=payload.timestamp,
    )
    return _to_expense_response(expense)


@router.get("/{trip_id}/expenses", response_model=ExpenseListResponse)
def list_expenses(
    trip_id: uuid.UUID,
    user_id: uuid.UUID | None = Query(default=None),
    category: CategoryEnum | None = Query(default=None),
    day: date | None = Query(default=None),
    expense_service: ExpenseService = Depends(get_expense_service),
) -> ExpenseListResponse:
    expenses = expense_service.list_expenses(trip_id, user_id=user_id, category=category, day=day)
    return ExpenseListResponse(expenses=[_to_expense_response(e) for e in expenses])