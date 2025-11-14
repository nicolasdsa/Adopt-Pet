from __future__ import annotations

from typing import Iterable

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from models.animal_species import AnimalSpecies


class AnimalSpeciesRepository:
    """Consultas relacionadas aos tipos de animal."""

    def _base_query(self) -> Select[tuple[AnimalSpecies]]:
        return select(AnimalSpecies).order_by(AnimalSpecies.label)

    def list_all(self, db: Session) -> list[AnimalSpecies]:
        return list(db.execute(self._base_query()).scalars())

    def get_by_id(self, db: Session, species_id: int) -> AnimalSpecies | None:
        stmt = self._base_query().where(AnimalSpecies.id == species_id)
        return db.execute(stmt).unique().scalar_one_or_none()

    def get_by_slugs(self, db: Session, slugs: Iterable[str]) -> list[AnimalSpecies]:
        slugs = list(slugs)
        if not slugs:
            return []
        stmt = self._base_query().where(AnimalSpecies.slug.in_(slugs))
        return list(db.execute(stmt).scalars())
