from __future__ import annotations
from sqlalchemy.orm import Session

from models.animal import (
    Animal,
    AnimalSex,
    AnimalSize,
    AnimalStatus,
    EnvironmentPreference,
    SociableTarget,
    TemperamentTrait,
)
from models.animal_photo import AnimalPhoto
from models.animal_species import AnimalSpecies
from models.organization import Organization
from repositories.animal_repository import AnimalRepository
from repositories.animal_species_repository import AnimalSpeciesRepository
from schemas.animal import AnimalCreate, AnimalCharacteristicsRead


class AnimalSpeciesNotFoundError(Exception):
    """Raised when the informed animal species does not exist."""


class AnimalService:
    """Regras de negócio relacionadas aos animais."""

    _TEMPERAMENT_LABELS = {
        TemperamentTrait.docile: "Dócil",
        TemperamentTrait.playful: "Brincalhão",
        TemperamentTrait.calm: "Calmo",
        TemperamentTrait.shy: "Tímido",
        TemperamentTrait.protective: "Protetor",
        TemperamentTrait.energetic: "Energético",
    }
    _ENVIRONMENT_LABELS = {
        EnvironmentPreference.apartment: "Apartamento",
        EnvironmentPreference.house_with_yard: "Casa com quintal",
        EnvironmentPreference.farm_or_ranch: "Sítio / chácara",
        EnvironmentPreference.active_family: "Família ativa",
    }
    _SOCIABLE_LABELS = {
        SociableTarget.dogs: "Cachorros",
        SociableTarget.cats: "Gatos",
        SociableTarget.children: "Crianças",
        SociableTarget.unknown_people: "Desconhecidos",
        SociableTarget.elderly: "Idosos",
        SociableTarget.other_pets: "Outros pets",
    }

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

    def list_characteristics(self) -> AnimalCharacteristicsRead:
        def _options(enum_cls, labels: dict) -> list[dict[str, str]]:
            return [
                {"value": item.value, "label": labels.get(item, item.value)}
                for item in enum_cls
            ]

        return AnimalCharacteristicsRead(
            temperament_traits=_options(TemperamentTrait, self._TEMPERAMENT_LABELS),
            environment_preferences=_options(
                EnvironmentPreference, self._ENVIRONMENT_LABELS
            ),
            sociable_with=_options(SociableTarget, self._SOCIABLE_LABELS),
        )

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
            temperament_traits=payload.temperament_traits,
            environment_preferences=payload.environment_preferences,
            sociable_with=payload.sociable_with,
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

    def search_available_animals(
        self,
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
    ) -> list[tuple[Animal, float]]:
        effective_radius = radius_km if radius_km is not None else 50.0
        return self.animal_repository.search_available(
            db,
            latitude=latitude,
            longitude=longitude,
            radius_km=effective_radius,
            skip=skip,
            limit=limit,
            species_id=species_id,
            size=size,
            sex=sex,
            age_years=age_years,
            temperament_traits=temperament_traits,
        )

    def list_animals_by_organization(
        self,
        db: Session,
        *,
        organization: Organization,
        skip: int = 0,
        limit: int = 50,
        name: str | None = None,
        status: AnimalStatus | None = None,
    ) -> list[Animal]:
        return self.animal_repository.list_by_organization(
            db,
            organization_id=organization.id,
            skip=skip,
            limit=limit,
            name=name,
            status=status,
        )
