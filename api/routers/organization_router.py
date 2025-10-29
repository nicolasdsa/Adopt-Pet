from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from controllers.organization_controller import (
    create_organization,
    get_organization,
    list_organizations,
)
from db.session import get_db
from schemas.organization import OrganizationCreate, OrganizationRead

router = APIRouter(prefix="/ongs", tags=["ONGs"])


@router.post(
    "",
    response_model=OrganizationRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar uma nova ONG",
)
def register_organization(
    payload: OrganizationCreate, db: Session = Depends(get_db)
) -> OrganizationRead:
    """Cria um cadastro de ONG."""
    return create_organization(payload, db)


@router.get(
    "",
    response_model=list[OrganizationRead],
    summary="Listar ONGs cadastradas",
)
def list_registered_organizations(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[OrganizationRead]:
    """Retorna uma lista paginada de ONGs."""
    return list_organizations(db, skip=skip, limit=limit)


@router.get(
    "/{organization_id}",
    response_model=OrganizationRead,
    summary="Detalhar uma ONG específica",
)
def retrieve_organization(
    organization_id: UUID, db: Session = Depends(get_db)
) -> OrganizationRead:
    """Busca informações da ONG pelo ID."""
    return get_organization(organization_id, db)
