from __future__ import annotations
from sqlalchemy.orm import Session

from models.animal import Animal
from models.animal_photo import AnimalPhoto
from models.animal_species import AnimalSpecies
from models.organization import Organization
from repositories.animal_repository import AnimalRepository
from repositories.animal_species_repository import AnimalSpeciesRepository
from schemas.animal import AnimalCreate


class AnimalSpeciesNotFoundError(Exception):
    """Raised when the informed animal species does not exist."""


class AnimalService:
    """Regras de negócio relacionadas aos animais."""

    def __init__(
        self,
        animal_repository: AnimalRepository | None = None,
        animal_species_repository: AnimalSpeciesRepository | None = None,
    ) -> None:
        self.animal_repository = animal_repository or AnimalRepository()
        self.animal_species_repository = (
            animal_species_repository or AnimalSpeciesRepository()
        )

    def list_species(self, db: Session) -> list[AnimalSpecies]:
        return self.animal_species_repository.list_all(db)

    def create_animal(
        self,
        db: Session,
        organization: Organization,
        payload: AnimalCreate,
    ) -> Animal:
        species = self.animal_species_repository.get_by_id(db, payload.species_id)
        if species is None:
            raise AnimalSpeciesNotFoundError

        animal = Animal(
            organization_id=organization.id,
            name=payload.name,
            species_id=payload.species_id,
            sex=payload.sex,
            age_years=payload.age_years,
            weight_kg=payload.weight_kg,
            size=payload.size,
            temperament=payload.temperament,
            vaccinated=payload.vaccinated,
            neutered=payload.neutered,
            dewormed=payload.dewormed,
            rescue_date=payload.rescue_date,
            microchip=payload.microchip,
            description=payload.description,
            adoption_requirements=payload.adoption_requirements,
            status=payload.status,
        )
        animal.species = species
        animal.photos = [
            AnimalPhoto(url=str(photo.url), position=photo.position)
            for photo in payload.photos
        ]

        self.animal_repository.add(db, animal)
        try:
            db.commit()
        except Exception:
            db.rollback()
            raise

        db.refresh(animal)
        return animal
