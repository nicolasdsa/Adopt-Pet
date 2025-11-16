from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.animal import (
    Animal,
    AnimalSex,
    AnimalSize,
    AnimalStatus,
    TemperamentTrait,
)
from models.organization import Organization
from schemas.animal import (
    AnimalCharacteristicsRead,
    AnimalCreate,
    AnimalListItemRead,
    AnimalPhotoRead,
    AnimalRead,
    AnimalOrganizationSummary,
    AnimalPublicRead,
    AnimalSpeciesRead,
)
from services.animal_service import AnimalService, AnimalSpeciesNotFoundError

service = AnimalService()


def create_animal(
    payload: AnimalCreate,
    *,
    organization: Organization,
    db: Session,
) -> AnimalRead:
    try:
        animal = service.create_animal(db, organization, payload)
    except AnimalSpeciesNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de animal não encontrado.",
        )
    return _serialize(animal)


def list_species(db: Session) -> list[AnimalSpeciesRead]:
    species = service.list_species(db)
    return [AnimalSpeciesRead.model_validate(item) for item in species]


def list_characteristics() -> AnimalCharacteristicsRead:
    return service.list_characteristics()


def list_animals_by_organization(
    db: Session,
    *,
    organization: Organization,
    skip: int = 0,
    limit: int = 50,
    name: str | None = None,
    status: AnimalStatus | None = None,
) -> list[AnimalListItemRead]:
    animals = service.list_animals_by_organization(
        db,
        organization=organization,
        skip=skip,
        limit=limit,
        name=name,
        status=status,
    )
    return [_serialize_list_item(animal) for animal in animals]


def search_available_animals(
    db: Session,
    *,
    latitude: float,
    longitude: float,
    skip: int = 0,
    limit: int = 50,
    radius_km: float | None = None,
    species_id: int | None = None,
    size: AnimalSize | None = None,
    sex: AnimalSex | None = None,
    age_years: int | None = None,
    temperament_traits: list[TemperamentTrait] | None = None,
) -> list[AnimalPublicRead]:
    animals = service.search_available_animals(
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
    return [_serialize_public(animal, distance) for animal, distance in animals]


def _serialize(animal: Animal) -> AnimalRead:
    return AnimalRead(
        id=animal.id,
        organization_id=animal.organization_id,
        name=animal.name,
        species=animal.species,
        sex=animal.sex,
        age_years=animal.age_years,
        weight_kg=animal.weight_kg,
        size=animal.size,
        temperament_traits=animal.temperament_traits,
        environment_preferences=animal.environment_preferences,
        sociable_with=animal.sociable_with,
        vaccinated=animal.vaccinated,
        neutered=animal.neutered,
        dewormed=animal.dewormed,
        rescue_date=animal.rescue_date,
        microchip=animal.microchip,
        description=animal.description,
        adoption_requirements=animal.adoption_requirements,
        status=animal.status,
        created_at=animal.created_at,
        updated_at=animal.updated_at,
        photos=[
            AnimalPhotoRead(
                id=photo.id,
                url=photo.url,
                position=photo.position,
                created_at=photo.created_at,
            )
            for photo in sorted(
                animal.photos,
                key=lambda photo: (
                    photo.position is None,
                    photo.position or 0,
                    photo.created_at,
                ),
            )
        ],
    )


def _serialize_list_item(animal: Animal) -> AnimalListItemRead:
    first_photo = animal.photos[0] if animal.photos else None
    return AnimalListItemRead(
        id=animal.id,
        name=animal.name,
        status=animal.status,
        species=animal.species,
        photo_url=first_photo.url if first_photo else None,
    )


def _serialize_public(animal: Animal, distance_km: float) -> AnimalPublicRead:
    if animal.organization is None:
        raise ValueError("Animal não possui ONG associada.")

    return AnimalPublicRead(
        **_serialize(animal).model_dump(),
        distance_km=distance_km,
        organization=_serialize_organization_summary(animal.organization),
    )


def _serialize_organization_summary(
    organization: Organization,
) -> AnimalOrganizationSummary:
    return AnimalOrganizationSummary(
        id=organization.id,
        name=organization.name,
        city=organization.city,
        state=organization.state,
        latitude=_to_float(organization.latitude),
        longitude=_to_float(organization.longitude),
        logo_url=organization.logo_url,
    )


def _to_float(value: float | None) -> float | None:
    return float(value) if value is not None else None
