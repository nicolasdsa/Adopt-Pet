from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.expense_category import ExpenseCategory
from models.organization import Organization
from schemas.expense_category import ExpenseCategoryCreate, ExpenseCategoryRead
from services.expense_category_service import (
    ExpenseCategoryDeleteForbiddenError,
    ExpenseCategoryHasExpensesError,
    ExpenseCategoryInvalidKeyError,
    ExpenseCategoryNameConflictError,
    ExpenseCategoryNotFoundError,
    ExpenseCategoryService,
)

service = ExpenseCategoryService()


def list_categories(
    organization: Organization, db: Session
) -> list[ExpenseCategoryRead]:
    categories = service.list_categories(db, organization)
    return [_serialize(category) for category in categories]


def create_category(
    organization: Organization, payload: ExpenseCategoryCreate, db: Session
) -> ExpenseCategoryRead:
    try:
        category = service.create_category(db, organization, payload)
    except ExpenseCategoryInvalidKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A chave da categoria é inválida.",
        )
    except ExpenseCategoryNameConflictError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe uma categoria com esta chave.",
        )
    return _serialize(category)


def delete_category(
    organization: Organization, category_id: UUID, db: Session
) -> None:
    try:
        service.delete_category(db, organization, category_id)
    except ExpenseCategoryNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria não encontrada.",
        )
    except ExpenseCategoryDeleteForbiddenError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não é permitido excluir esta categoria.",
        )
    except ExpenseCategoryHasExpensesError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A categoria possui despesas vinculadas.",
        )


def _serialize(category: ExpenseCategory) -> ExpenseCategoryRead:
    return ExpenseCategoryRead.model_validate(category)
