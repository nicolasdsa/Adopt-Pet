from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from controllers.expense_controller import create_expense, get_expense, list_expenses
from core.dependencies import get_current_organization
from db.session import get_db
from models.organization import Organization
from schemas.expense import ExpenseCreate, ExpenseRead

router = APIRouter(prefix="/expenses", tags=["Despesas"])


@router.post(
    "",
    response_model=ExpenseRead,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar uma nova despesa",
)
def register_expense(
    payload: ExpenseCreate,
    organization: Organization = Depends(get_current_organization),
    db: Session = Depends(get_db),
) -> ExpenseRead:
    return create_expense(organization, payload, db)


@router.get(
    "",
    response_model=list[ExpenseRead],
    summary="Listar despesas da ONG",
)
def list_organization_expenses(
    organization: Organization = Depends(get_current_organization),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    category_id: UUID | None = Query(None),
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
) -> list[ExpenseRead]:
    return list_expenses(
        organization,
        db,
        skip=skip,
        limit=limit,
        category_id=category_id,
        start_date=start_date,
        end_date=end_date,
    )


@router.get(
    "/{expense_id}",
    response_model=ExpenseRead,
    summary="Obter detalhes de uma despesa",
)
def retrieve_expense(
    expense_id: UUID,
    organization: Organization = Depends(get_current_organization),
    db: Session = Depends(get_db),
) -> ExpenseRead:
    return get_expense(organization, expense_id, db)
