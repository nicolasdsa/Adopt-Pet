from __future__ import annotations

from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session, joinedload, selectinload

from models.animal import (
    Animal,
    AnimalSex,
    AnimalSize,
    AnimalStatus,
    TemperamentTrait,
)
from models.organization import GeographyPoint, Organization


class AnimalRepository:
    """Operações de persistência relacionadas aos animais."""

    def _base_query(self) -> Select[tuple[Animal]]:
        return select(Animal).options(
            selectinload(Animal.photos), selectinload(Animal.species)
        )

    def add(self, db: Session, animal: Animal) -> Animal:
        db.add(animal)
        return animal

    def get_by_id(self, db: Session, animal_id: UUID) -> Animal | None:
        stmt = self._base_query().where(Animal.id == animal_id)
        return db.execute(stmt).unique().scalar_one_or_none()

    def list_by_organization(
        self,
        db: Session,
        organization_id: UUID,
        *,
        skip: int = 0,
        limit: int = 50,
        name: str | None = None,
        status: AnimalStatus | None = None,
    ) -> list[Animal]:
        stmt = (
            self._base_query()
            .where(Animal.organization_id == organization_id)
            .order_by(Animal.created_at.desc())
            .offset(skip)
            .limit(limit)
        )

        if name:
            clean_name = name.strip()
            if clean_name:
                stmt = stmt.where(Animal.name.ilike(f"%{clean_name}%"))
        if status is not None:
            stmt = stmt.where(Animal.status == status)

        return list(db.execute(stmt).scalars())

    def search_available(
        self,
        db: Session,
        *,
        latitude: float,
        longitude: float,
        radius_km: float,
        skip: int = 0,
        limit: int = 50,
        species_id: int | None = None,
        size: AnimalSize | None = None,
        sex: AnimalSex | None = None,
        age_years: int | None = None,
        temperament_traits: list[TemperamentTrait] | None = None,
    ) -> list[tuple[Animal, float]]:
        reference_point = func.ST_SetSRID(
            func.ST_MakePoint(longitude, latitude),
            4326,
        )
        reference_point_geog = func.cast(reference_point, GeographyPoint())
        distance_expr = (
            func.ST_Distance(Organization.location, reference_point_geog) / 1000.0
        ).label("distance_km")

        stmt = (
            select(Animal, distance_expr)
            .join(Organization, Animal.organization_id == Organization.id)
            .options(
                selectinload(Animal.photos),
                selectinload(Animal.species),
                joinedload(Animal.organization),
            )
            .where(Animal.status == AnimalStatus.available)
            .where(Organization.location.isnot(None))
            .where(
                func.ST_DWithin(
                    Organization.location,
                    reference_point_geog,
                    radius_km * 1000.0,
                )
            )
        )

        if species_id is not None:
            stmt = stmt.where(Animal.species_id == species_id)
        if size is not None:
            stmt = stmt.where(Animal.size == size)
        if sex is not None:
            stmt = stmt.where(Animal.sex == sex)
        if age_years is not None:
            stmt = stmt.where(Animal.age_years == age_years)
        if temperament_traits:
            stmt = stmt.where(Animal.temperament_traits.contains(temperament_traits))

        stmt = (
            stmt.order_by(distance_expr, Animal.created_at.desc())
            .offset(skip)
            .limit(limit)
        )

        results = db.execute(stmt).unique().all()
        return [
            (animal, float(distance_km or 0.0))
            for animal, distance_km in results
        ]
