from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class AdoptionStatsRead(BaseModel):
    current_month_total: int = Field(0, ge=0)
    average_days_to_adoption: float | None = Field(
        None,
        ge=0,
        description="Tempo médio (em dias) para adoção desde o cadastro.",
    )
    return_rate: float = Field(
        0,
        ge=0,
        description="Proporção de adoções que foram encerradas/devolvidas.",
    )


class ExpensesHighlightRead(BaseModel):
    current_month_total: Decimal = Field(0, ge=0)
    previous_month_total: Decimal = Field(0, ge=0)
    variation_percentage: float = Field(
        0,
        description="Variação percentual entre os dois períodos.",
    )


class ExpensesByCategoryRead(BaseModel):
    category_id: UUID
    category_name: str = Field(..., max_length=100)
    total: Decimal = Field(0, ge=0)


class DashboardSummaryRead(BaseModel):
    active_animals: int = Field(0, ge=0)
    adoptions: AdoptionStatsRead
    volunteers_active: int = Field(
        0,
        ge=0,
        description="Campo reservado até integração com módulo de voluntários.",
    )
    expenses: ExpensesHighlightRead
    expenses_by_category: list[ExpensesByCategoryRead]


__all__ = [
    "AdoptionStatsRead",
    "ExpensesHighlightRead",
    "ExpensesByCategoryRead",
    "DashboardSummaryRead",
]
