from __future__ import annotations

from dataclasses import dataclass
import re
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.expense_category import ExpenseCategory
from models.organization import Organization
from repositories.expense_category_repository import ExpenseCategoryRepository
from schemas.expense_category import ExpenseCategoryCreate


class ExpenseCategoryNameConflictError(Exception):
    """Raised when a category with the same key already exists."""


class ExpenseCategoryNotFoundError(Exception):
    """Raised when the requested category does not exist."""


class ExpenseCategoryDeleteForbiddenError(Exception):
    """Raised when attempting to remove a category that cannot be deleted."""


class ExpenseCategoryHasExpensesError(Exception):
    """Raised when trying to delete a category that is in use by expenses."""


class ExpenseCategoryInvalidKeyError(Exception):
    """Raised when the provided key is invalid."""


@dataclass(slots=True)
class ExpenseCategoryService:
    """Regras de negócio para categorias de despesas."""

    repository: ExpenseCategoryRepository = ExpenseCategoryRepository()

    def list_categories(
        self, db: Session, organization: Organization
    ) -> list[ExpenseCategory]:
        return self.repository.list_for_organization(db, organization.id)

    def create_category(
        self, db: Session, organization: Organization, payload: ExpenseCategoryCreate
    ) -> ExpenseCategory:
        normalized_key = self._normalize_key(payload.key)

        if self.repository.exists_with_key(
            db, organization_id=organization.id, key=normalized_key
        ):
            raise ExpenseCategoryNameConflictError

        category = ExpenseCategory(
            organization_id=organization.id,
            key=normalized_key,
            name=payload.name.strip(),
            icon=payload.icon,
        )

        self.repository.add(db, category)
        try:
            db.commit()
        except IntegrityError as exc:
            db.rollback()
            raise ExpenseCategoryNameConflictError from exc

        db.refresh(category)
        return category

    def delete_category(
        self, db: Session, organization: Organization, category_id: UUID
    ) -> None:
        category = self.repository.get_by_id(db, category_id)
        if category is None:
            raise ExpenseCategoryNotFoundError
        if category.organization_id is None or category.organization_id != organization.id:
            raise ExpenseCategoryDeleteForbiddenError

        if self.repository.count_expenses(db, category_id) > 0:
            raise ExpenseCategoryHasExpensesError

        self.repository.delete(db, category)
        db.commit()

    @staticmethod
    def _normalize_key(raw_key: str) -> str:
        key = re.sub(r"[^a-z0-9]+", "-", raw_key.strip().lower()).strip("-")
        if not key:
            raise ExpenseCategoryInvalidKeyError
        return key
