from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlalchemy import Select, and_, func, select
from sqlalchemy.orm import Session, joinedload, selectinload

from models.expense import Expense
from models.expense_category import ExpenseCategory


class ExpenseRepository:
    """Operações de persistência relacionadas às despesas."""

    def _base_query(self) -> Select[tuple[Expense]]:
        return select(Expense).options(
            joinedload(Expense.category),
            selectinload(Expense.attachments),
        )

    def add(self, db: Session, expense: Expense) -> Expense:
        db.add(expense)
        return expense

    def list_by_organization(
        self,
        db: Session,
        organization_id: UUID,
        *,
        skip: int = 0,
        limit: int = 50,
        category_id: UUID | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[Expense]:
        stmt = (
            self._base_query()
            .where(Expense.organization_id == organization_id)
            .order_by(Expense.expense_date.desc(), Expense.created_at.desc())
            .offset(skip)
            .limit(limit)
        )

        if category_id is not None:
            stmt = stmt.where(Expense.category_id == category_id)
        if start_date is not None:
            stmt = stmt.where(Expense.expense_date >= start_date)
        if end_date is not None:
            stmt = stmt.where(Expense.expense_date <= end_date)

        return list(db.execute(stmt).scalars())

    def get_by_id_for_organization(
        self, db: Session, expense_id: UUID, organization_id: UUID
    ) -> Expense | None:
        stmt = self._base_query().where(
            and_(
                Expense.id == expense_id,
                Expense.organization_id == organization_id,
            )
        )
        return db.execute(stmt).unique().scalar_one_or_none()

    def totals_by_category(
        self,
        db: Session,
        organization_id: UUID,
        *,
        start_date: date,
        end_date: date,
    ) -> list[tuple[str, Decimal]]:
        stmt = (
            select(
                ExpenseCategory.name.label("name"),
                func.coalesce(func.sum(Expense.amount), 0).label("total"),
            )
            .join(ExpenseCategory, ExpenseCategory.id == Expense.category_id)
            .where(
                Expense.organization_id == organization_id,
                Expense.expense_date >= start_date,
                Expense.expense_date <= end_date,
            )
            .group_by(ExpenseCategory.name)
            .order_by(ExpenseCategory.name)
        )
        rows = db.execute(stmt).all()
        return [
            (row.name, Decimal(row.total or 0))
            for row in rows
        ]
