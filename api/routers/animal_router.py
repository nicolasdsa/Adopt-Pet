from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from controllers.animal_controller import (
    create_animal,
    list_animals_by_organization,
    list_characteristics,
    search_available_animals,
    list_species,
)
from core.dependencies import get_current_organization
from db.session import get_db
from models.organization import Organization
from models.animal import AnimalSex, AnimalSize, AnimalStatus, TemperamentTrait
from schemas.animal import (
    AnimalCharacteristicsRead,
    AnimalCreate,
    AnimalListItemRead,
    AnimalPublicRead,
    AnimalRead,
    AnimalSpeciesRead,
)

router = APIRouter(prefix="/animals", tags=["Animais"])


@router.get(
    "",
    response_model=list[AnimalPublicRead],
    summary="Listar animais disponíveis próximos",
)
def list_available_animals_route(
    latitude: float = Query(
        ...,
        ge=-90,
        le=90,
        description="Latitude em graus decimais (WGS84).",
    ),
    longitude: float = Query(
        ...,
        ge=-180,
        le=180,
        description="Longitude em graus decimais (WGS84).",
    ),
    radius_km: float = Query(
        50.0,
        gt=0,
        le=500,
        description="Raio do filtro geográfico em quilômetros. Padrão 50 km.",
    ),
    species_id: int | None = Query(
        None,
        ge=1,
        description="Filtrar por ID da espécie retornado no catálogo.",
    ),
    size: AnimalSize | None = Query(
        None,
        description="Filtrar por porte (small, medium, large).",
    ),
    sex: AnimalSex | None = Query(
        None,
        description="Filtrar por sexo do animal.",
    ),
    age_years: int | None = Query(
        None,
        ge=0,
        le=50,
        description="Idade em anos completos.",
    ),
    temperament_traits: list[TemperamentTrait] | None = Query(
        None,
        description="Informe múltiplas vezes para combinar temperamentos desejados.",
    ),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[AnimalPublicRead]:
    return search_available_animals(
        db,
        latitude=latitude,
        longitude=longitude,
        skip=skip,
        limit=limit,
        radius_km=radius_km,
        species_id=species_id,
        size=size,
        sex=sex,
        age_years=age_years,
        temperament_traits=temperament_traits,
    )


@router.get(
    "/mine",
    response_model=list[AnimalListItemRead],
    summary="Listar animais da ONG autenticada",
)
def list_organization_animals_route(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    name: str | None = Query(
        None,
        min_length=1,
        max_length=255,
        description="Filtro parcial pelo nome do animal.",
    ),
    status: AnimalStatus | None = Query(
        None,
        description="Filtrar pelo status atual (available, reserved, etc).",
    ),
    db: Session = Depends(get_db),
    organization: Organization = Depends(get_current_organization),
) -> list[AnimalListItemRead]:
    return list_animals_by_organization(
        db,
        organization=organization,
        skip=skip,
        limit=limit,
        name=name,
        status=status,
    )


@router.get(
    "/species",
    response_model=list[AnimalSpeciesRead],
    summary="Listar espécies de animais disponíveis",
)
def list_animal_species(db: Session = Depends(get_db)) -> list[AnimalSpeciesRead]:
    """Retorna as espécies cadastradas para seleção."""
    return list_species(db)


@router.get(
    "/characteristics",
    response_model=AnimalCharacteristicsRead,
    summary="Listar opções de características para cadastro",
)
def list_animal_characteristics() -> AnimalCharacteristicsRead:
    """Retorna os valores dos enumeradores usados nos chips do formulário."""
    return list_characteristics()


@router.post(
    "",
    response_model=AnimalRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar um novo animal",
)
def register_animal(
    payload: AnimalCreate,
    db: Session = Depends(get_db),
    organization: Organization = Depends(get_current_organization),
) -> AnimalRead:
    """Registra um animal vinculado a uma ONG."""
    return create_animal(payload, organization=organization, db=db)
