from __future__ import annotations

from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.orm import Session, selectinload

from models.animal import Animal


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
        return db.execute(stmt).scalar_one_or_none()

    def list_by_organization(
        self,
        db: Session,
        organization_id: UUID,
        *,
        skip: int = 0,
        limit: int = 50,
    ) -> list[Animal]:
        stmt = (
            self._base_query()
            .where(Animal.organization_id == organization_id)
            .order_by(Animal.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(db.execute(stmt).scalars())
