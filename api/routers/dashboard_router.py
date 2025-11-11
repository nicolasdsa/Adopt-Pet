from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from controllers.dashboard_controller import get_dashboard_summary
from core.dependencies import get_current_organization
from db.session import get_db
from models.organization import Organization
from schemas.dashboard import DashboardSummaryRead

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get(
    "",
    response_model=DashboardSummaryRead,
    summary="Resumo consolidado para o painel da ONG",
)
def read_dashboard_summary(
    db: Session = Depends(get_db),
    organization: Organization = Depends(get_current_organization),
) -> DashboardSummaryRead:
    return get_dashboard_summary(db=db, organization=organization)


__all__ = ["router"]
