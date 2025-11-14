from __future__ import annotations

from uuid import UUID

from sqlalchemy import Select, and_, func, select
from sqlalchemy.orm import Session

from models.expense_category import ExpenseCategory


class ExpenseCategoryRepository:
    """Consultas relacionadas às categorias de despesa."""

    def _base_query(self) -> Select[tuple[ExpenseCategory]]:
        return select(ExpenseCategory)

    def add(self, db: Session, category: ExpenseCategory) -> ExpenseCategory:
        db.add(category)
        return category

    def get_by_id(self, db: Session, category_id: UUID) -> ExpenseCategory | None:
        stmt = self._base_query().where(ExpenseCategory.id == category_id)
        return db.execute(stmt).unique().scalar_one_or_none()

    def get_owned_by_organization(
        self, db: Session, category_id: UUID, organization_id: UUID
    ) -> ExpenseCategory | None:
        stmt = self._base_query().where(
            and_(
                ExpenseCategory.id == category_id,
                ExpenseCategory.organization_id == organization_id,
            )
        )
        return db.execute(stmt).scalar_one_or_none()

    def list_for_organization(
        self, db: Session, organization_id: UUID
    ) -> list[ExpenseCategory]:
        stmt = (
            self._base_query()
            .where(
                (ExpenseCategory.organization_id == organization_id)
                | (ExpenseCategory.organization_id.is_(None))
            )
            .order_by(ExpenseCategory.name.asc())
        )
        return list(db.execute(stmt).scalars())

    def exists_with_key(
        self, db: Session, *, organization_id: UUID, key: str
    ) -> bool:
        stmt = select(func.count(ExpenseCategory.id)).where(
            and_(
                func.lower(ExpenseCategory.key) == func.lower(key),
                (ExpenseCategory.organization_id == organization_id)
                | (ExpenseCategory.organization_id.is_(None)),
            )
        )
        return db.execute(stmt).scalar_one() > 0

    def count_expenses(self, db: Session, category_id: UUID) -> int:
        from models.expense import Expense  # local import to avoid cycle

        stmt = select(func.count(Expense.id)).where(Expense.category_id == category_id)
        return db.execute(stmt).scalar_one()

    def delete(self, db: Session, category: ExpenseCategory) -> None:
        db.delete(category)
