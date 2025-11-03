from __future__ import annotations

from datetime import date
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.expense import Expense
from models.organization import Organization
from schemas.expense import ExpenseCreate, ExpenseRead
from services.expense_service import (
    ExpenseAnimalNotFoundError,
    ExpenseCategoryUnavailableError,
    ExpenseNotFoundError,
    ExpenseService,
)

service = ExpenseService()


def create_expense(
    organization: Organization, payload: ExpenseCreate, db: Session
) -> ExpenseRead:
    try:
        expense = service.create_expense(db, organization, payload)
    except ExpenseCategoryUnavailableError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria informada não disponível para a ONG.",
        )
    except ExpenseAnimalNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animal não encontrado para esta ONG.",
        )
    return _serialize(expense)


def list_expenses(
    organization: Organization,
    db: Session,
    *,
    skip: int = 0,
    limit: int = 50,
    category_id: UUID | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[ExpenseRead]:
    expenses = service.list_expenses(
        db,
        organization,
        skip=skip,
        limit=limit,
        category_id=category_id,
        start_date=start_date,
        end_date=end_date,
    )
    return [_serialize(expense) for expense in expenses]


def get_expense(
    organization: Organization, expense_id: UUID, db: Session
) -> ExpenseRead:
    try:
        expense = service.get_expense(db, organization, expense_id)
    except ExpenseNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Despesa não encontrada.",
        )
    return _serialize(expense)


def _serialize(expense: Expense) -> ExpenseRead:
    return ExpenseRead.model_validate(expense)
