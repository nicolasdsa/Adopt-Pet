from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.animal import Animal
from models.organization import Organization
from schemas.animal import (
    AnimalCharacteristicsRead,
    AnimalCreate,
    AnimalPhotoRead,
    AnimalRead,
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
