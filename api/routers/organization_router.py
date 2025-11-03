from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from controllers.organization_controller import (
    create_organization,
    get_organization,
    list_organizations,
    search_organizations,
)
from db.session import get_db
from schemas.organization import (
    HelpType,
    OrganizationCreate,
    OrganizationRead,
    OrganizationSearchRead,
)

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
    "/search",
    response_model=list[OrganizationSearchRead],
    summary="Buscar ONGs com filtros",
)
def search_ongs(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    name: str | None = Query(None, min_length=1, max_length=255),
    help_type: HelpType | None = Query(None),
    latitude: float | None = Query(
        None,
        ge=-90,
        le=90,
        description="Latitude em graus decimais (WGS84).",
    ),
    longitude: float | None = Query(
        None,
        ge=-180,
        le=180,
        description="Longitude em graus decimais (WGS84).",
    ),
    radius_km: float | None = Query(
        None,
        gt=0,
        description="Raio de busca em quilômetros. Padrão 25 km.",
    ),
    db: Session = Depends(get_db),
) -> list[OrganizationSearchRead]:
    """Busca ONGs por nome, tipo de ajuda e proximidade geográfica."""
    if (latitude is None) ^ (longitude is None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Latitude e longitude devem ser informadas em conjunto.",
        )

    return search_organizations(
        db,
        skip=skip,
        limit=limit,
        name=name,
        help_type=help_type,
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km,
    )


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
