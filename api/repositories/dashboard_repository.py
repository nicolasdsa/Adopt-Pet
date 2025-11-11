from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import Float, cast, func, select
from sqlalchemy.orm import Session

from models.adoption import Adoption
from models.animal import Animal, AnimalStatus
from models.expense import Expense
from models.expense_category import ExpenseCategory


@dataclass(frozen=True, slots=True)
class HeadlineMetrics:
    active_animals: int
    adoptions_current_month: int
    avg_days_until_adoption: float | None
    return_rate: float
    expenses_current_month: Decimal
    expenses_previous_month: Decimal


@dataclass(frozen=True, slots=True)
class ExpenseCategoryRow:
    category_id: UUID
    category_name: str
    total: Decimal


class DashboardRepository:
    """Consultas otimizadas para o painel da ONG."""

    def fetch_headline_metrics(
        self,
        db: Session,
        organization_id: UUID,
        *,
        current_start: datetime,
        current_end: datetime,
        previous_start: datetime,
        previous_end: datetime,
    ) -> HeadlineMetrics:
        current_start_date = current_start.date()
        current_end_date = current_end.date()
        previous_start_date = previous_start.date()
        previous_end_date = previous_end.date()

        active_animals = (
            select(func.count(Animal.id))
            .where(
                Animal.organization_id == organization_id,
                Animal.status.in_(
                    [AnimalStatus.available, AnimalStatus.reserved]
                ),
            )
            .scalar_subquery()
        )

        adoptions_current_month = (
            select(func.count(Adoption.id))
            .where(
                Adoption.organization_id == organization_id,
                Adoption.adoption_date >= current_start,
                Adoption.adoption_date < current_end,
            )
            .scalar_subquery()
        )

        avg_days_until_adoption = (
            select(
                func.avg(
                    func.extract(
                        "epoch",
                        Adoption.adoption_date - Animal.created_at,
                    )
                    / 86400.0
                )
            )
            .join(Animal, Animal.id == Adoption.animal_id)
            .where(Adoption.organization_id == organization_id)
            .scalar_subquery()
        )

        total_adoptions = (
            select(func.count(Adoption.id))
            .where(Adoption.organization_id == organization_id)
            .scalar_subquery()
        )
        returned_adoptions = (
            select(func.count(Adoption.id))
            .where(
                Adoption.organization_id == organization_id,
                Adoption.closed_at.isnot(None),
            )
            .scalar_subquery()
        )
        return_rate = func.coalesce(
            cast(returned_adoptions, Float)
            / func.nullif(cast(total_adoptions, Float), 0.0),
            0.0,
        )

        expenses_current_month = (
            select(func.coalesce(func.sum(Expense.amount), 0))
            .where(
                Expense.organization_id == organization_id,
                Expense.expense_date >= current_start_date,
                Expense.expense_date < current_end_date,
            )
            .scalar_subquery()
        )

        expenses_previous_month = (
            select(func.coalesce(func.sum(Expense.amount), 0))
            .where(
                Expense.organization_id == organization_id,
                Expense.expense_date >= previous_start_date,
                Expense.expense_date < previous_end_date,
            )
            .scalar_subquery()
        )

        stmt = select(
            active_animals.label("active_animals"),
            adoptions_current_month.label("adoptions_current_month"),
            avg_days_until_adoption.label("avg_days_until_adoption"),
            return_rate.label("return_rate"),
            expenses_current_month.label("expenses_current_month"),
            expenses_previous_month.label("expenses_previous_month"),
        )

        result = db.execute(stmt).one()
        return HeadlineMetrics(
            active_animals=int(result.active_animals or 0),
            adoptions_current_month=int(result.adoptions_current_month or 0),
            avg_days_until_adoption=(
                float(result.avg_days_until_adoption)
                if result.avg_days_until_adoption is not None
                else None
            ),
            return_rate=float(result.return_rate or 0.0),
            expenses_current_month=Decimal(result.expenses_current_month or 0),
            expenses_previous_month=Decimal(result.expenses_previous_month or 0),
        )

    def fetch_expenses_by_category(
        self,
        db: Session,
        organization_id: UUID,
        *,
        current_start_date: date,
        current_end_date: date,
    ) -> list[ExpenseCategoryRow]:
        stmt = (
            select(
                Expense.category_id,
                ExpenseCategory.name.label("category_name"),
                func.coalesce(func.sum(Expense.amount), 0).label("total"),
            )
            .join(
                ExpenseCategory,
                ExpenseCategory.id == Expense.category_id,
            )
            .where(
                Expense.organization_id == organization_id,
                Expense.expense_date >= current_start_date,
                Expense.expense_date < current_end_date,
            )
            .group_by(Expense.category_id, ExpenseCategory.name)
            .order_by(func.sum(Expense.amount).desc())
        )
        rows = db.execute(stmt).all()
        return [
            ExpenseCategoryRow(
                category_id=row.category_id,
                category_name=row.category_name,
                total=Decimal(row.total or 0),
            )
            for row in rows
        ]


__all__ = ["DashboardRepository", "HeadlineMetrics", "ExpenseCategoryRow"]
