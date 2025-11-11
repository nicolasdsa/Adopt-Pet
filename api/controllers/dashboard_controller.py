from __future__ import annotations

from fastapi import Depends
from sqlalchemy.orm import Session

from core.dependencies import get_current_organization
from db.session import get_db
from models.organization import Organization
from schemas.dashboard import DashboardSummaryRead
from services.dashboard_service import DashboardService

service = DashboardService()


def get_dashboard_summary(
    db: Session = Depends(get_db),
    organization: Organization = Depends(get_current_organization),
) -> DashboardSummaryRead:
    """Retorna os números consolidados para o painel da ONG autenticada."""
    return service.get_summary(db, organization.id)


__all__ = ["get_dashboard_summary"]
