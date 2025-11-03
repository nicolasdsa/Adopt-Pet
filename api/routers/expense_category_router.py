from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from controllers.expense_category_controller import (
    create_category,
    delete_category,
    list_categories,
)
from core.dependencies import get_current_organization
from db.session import get_db
from models.organization import Organization
from schemas.expense_category import ExpenseCategoryCreate, ExpenseCategoryRead

router = APIRouter(prefix="/expense-categories", tags=["Categorias de Despesas"])


@router.get(
    "",
    response_model=list[ExpenseCategoryRead],
    summary="Listar categorias acessíveis pela ONG",
)
def list_expense_categories(
    organization: Organization = Depends(get_current_organization),
    db: Session = Depends(get_db),
) -> list[ExpenseCategoryRead]:
    return list_categories(organization, db)


@router.post(
    "",
    response_model=ExpenseCategoryRead,
    status_code=status.HTTP_201_CREATED,
    summary="Criar uma categoria exclusiva da ONG",
)
def create_expense_category(
    payload: ExpenseCategoryCreate,
    organization: Organization = Depends(get_current_organization),
    db: Session = Depends(get_db),
) -> ExpenseCategoryRead:
    return create_category(organization, payload, db)


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir uma categoria da ONG",
)
def delete_expense_category(
    category_id: UUID,
    organization: Organization = Depends(get_current_organization),
    db: Session = Depends(get_db),
) -> None:
    delete_category(organization, category_id, db)
