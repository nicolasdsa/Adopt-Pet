from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.organization import Organization
from schemas.organization import (
    HelpType as HelpTypeEnum,
    OrganizationCreate,
    OrganizationRead,
    OrganizationSearchRead,
)
from services.organization_service import (
    DuplicateCNPJError,
    HelpTypeNotFoundError,
    OrganizationNotFoundError,
    OrganizationService,
)

service = OrganizationService()


def create_organization(payload: OrganizationCreate, db: Session) -> OrganizationRead:
    try:
        organization = service.create_organization(db, payload)
    except DuplicateCNPJError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe uma ONG cadastrada com este CNPJ.",
        )
    except HelpTypeNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    return _serialize(organization)


def list_organizations(
    db: Session, *, skip: int = 0, limit: int = 50
) -> list[OrganizationRead]:
    organizations = service.list_organizations(db, skip=skip, limit=limit)
    return [_serialize(organization) for organization in organizations]


def search_organizations(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 50,
    name: str | None = None,
    help_types: list[HelpTypeEnum] | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
    radius_km: float | None = None,
) -> list[OrganizationSearchRead]:
    results = service.search_organizations(
        db,
        skip=skip,
        limit=limit,
        name=name,
        help_types=help_types,
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km,
    )
    return [
        _serialize_search(organization, distance, dogs_count, cats_count)
        for organization, distance, dogs_count, cats_count in results
    ]


def get_organization(organization_id: UUID, db: Session) -> OrganizationRead:
    try:
        organization = service.get_organization(db, organization_id)
    except OrganizationNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ONG não encontrada.",
        )
    return _serialize(organization)


def _serialize(organization: Organization) -> OrganizationRead:
    return OrganizationRead(
        id=organization.id,
        name=organization.name,
        cnpj=organization.cnpj,
        address=organization.address,
        city=organization.city,
        state=organization.state,
        phone=organization.phone,
        email=organization.email,
        website=organization.website,
        instagram=organization.instagram,
        mission=organization.mission,
        help_types=[HelpTypeEnum(help_type.key) for help_type in organization.help_types],
        logo_url=organization.logo_url,
        accepts_terms=organization.accepts_terms,
        latitude=_to_float(organization.latitude),
        longitude=_to_float(organization.longitude),
        created_at=organization.created_at,
        updated_at=organization.updated_at,
    )


def _serialize_search(
    organization: Organization,
    distance_km: float | None,
    dogs_count: int,
    cats_count: int,
) -> OrganizationSearchRead:
    return OrganizationSearchRead(
        **_serialize(organization).model_dump(),
        distance_km=_to_float(distance_km),
        dogs_count=dogs_count,
        cats_count=cats_count,
    )


def _to_float(value: float | None) -> float | None:
    return float(value) if value is not None else None
