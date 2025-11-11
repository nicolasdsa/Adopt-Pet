from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from repositories.dashboard_repository import (
    DashboardRepository,
    ExpenseCategoryRow,
    HeadlineMetrics,
)
from schemas.dashboard import (
    AdoptionStatsRead,
    DashboardSummaryRead,
    ExpensesByCategoryRead,
    ExpensesHighlightRead,
)


@dataclass(slots=True)
class DashboardService:
    """Orquestra as consultas e cálculos para o painel da ONG."""

    repository: DashboardRepository = DashboardRepository()

    def get_summary(self, db: Session, organization_id: UUID) -> DashboardSummaryRead:
        current_start = self._start_of_month(datetime.now(timezone.utc))
        current_end = self._shift_month(current_start, 1)
        previous_start = self._shift_month(current_start, -1)
        previous_end = current_start

        headline = self.repository.fetch_headline_metrics(
            db,
            organization_id,
            current_start=current_start,
            current_end=current_end,
            previous_start=previous_start,
            previous_end=previous_end,
        )
        categories = self.repository.fetch_expenses_by_category(
            db,
            organization_id,
            current_start_date=current_start.date(),
            current_end_date=current_end.date(),
        )

        return DashboardSummaryRead(
            active_animals=headline.active_animals,
            adoptions=AdoptionStatsRead(
                current_month_total=headline.adoptions_current_month,
                average_days_to_adoption=headline.avg_days_until_adoption,
                return_rate=headline.return_rate,
            ),
            volunteers_active=0,  # aguardando módulo de voluntários
            expenses=ExpensesHighlightRead(
                current_month_total=headline.expenses_current_month,
                previous_month_total=headline.expenses_previous_month,
                variation_percentage=self._calculate_variation(
                    headline.expenses_current_month,
                    headline.expenses_previous_month,
                ),
            ),
            expenses_by_category=self._serialize_categories(categories),
        )

    def _calculate_variation(
        self, current_value: Decimal, previous_value: Decimal
    ) -> float:
        if previous_value == 0:
            return 100.0 if current_value > 0 else 0.0
        delta = (current_value - previous_value) / previous_value
        return round(float(delta * 100), 2)

    def _start_of_month(self, dt: datetime) -> datetime:
        return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    def _shift_month(self, dt: datetime, offset: int) -> datetime:
        month_index = dt.month - 1 + offset
        year = dt.year + month_index // 12
        month = month_index % 12 + 1
        return dt.replace(year=year, month=month, day=1)

    def _serialize_categories(
        self, rows: list[ExpenseCategoryRow]
    ) -> list[ExpensesByCategoryRead]:
        return [
            ExpensesByCategoryRead(
                category_id=row.category_id,
                category_name=row.category_name,
                total=row.total,
            )
            for row in rows
        ]


__all__ = ["DashboardService"]
