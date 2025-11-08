from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session, joinedload

from models.animal import Animal
from models.animal_species import AnimalSpecies
from models.help_type import HelpType
from models.organization import GeographyPoint, Organization


class OrganizationRepository:
    """Operações de persistência para organizações."""

    def _base_query(self) -> Select[tuple[Organization]]:
        return select(Organization).options(joinedload(Organization.help_types))

    def add(self, db: Session, organization: Organization) -> Organization:
        db.add(organization)
        return organization

    def list(
        self, db: Session, *, skip: int = 0, limit: int = 50
    ) -> list[Organization]:
        stmt = (
            self._base_query()
            .order_by(Organization.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(db.execute(stmt).scalars())

    def get_by_id(self, db: Session, organization_id: UUID) -> Organization | None:
        stmt = self._base_query().where(Organization.id == organization_id)
        return db.execute(stmt).scalar_one_or_none()

    def get_by_email(self, db: Session, email: str) -> Organization | None:
        stmt = self._base_query().where(Organization.email == email)
        return db.execute(stmt).scalar_one_or_none()

    def search(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 50,
        name: str | None = None,
        help_type_keys: list[str] | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
        radius_km: float | None = None,
    ) -> list[tuple[Organization, float | None, int, int]]:
        stmt = self._base_query()

        dogs_count = (
            select(func.count(Animal.id))
            .select_from(Animal)
            .join(AnimalSpecies, Animal.species_id == AnimalSpecies.id)
            .where(Animal.organization_id == Organization.id)
            .where(AnimalSpecies.slug == "dog")
            .correlate(Organization)
            .scalar_subquery()
            .label("dogs_count")
        )
        cats_count = (
            select(func.count(Animal.id))
            .select_from(Animal)
            .join(AnimalSpecies, Animal.species_id == AnimalSpecies.id)
            .where(Animal.organization_id == Organization.id)
            .where(AnimalSpecies.slug == "cat")
            .correlate(Organization)
            .scalar_subquery()
            .label("cats_count")
        )

        stmt = stmt.add_columns(dogs_count, cats_count)

        if name:
            clean_name = name.strip()
            if clean_name:
                stmt = stmt.where(Organization.name.ilike(f"%{clean_name}%"))

        if help_type_keys:
            stmt = stmt.where(
                Organization.help_types.any(HelpType.key.in_(help_type_keys))
            )

        distance_expr = None
        if latitude is not None and longitude is not None:
            radius_meters = (radius_km or 25.0) * 1000.0
            reference_point = func.ST_SetSRID(
                func.ST_MakePoint(longitude, latitude),
                4326,
            )
            reference_point_geog = func.cast(reference_point, GeographyPoint())
            stmt = stmt.where(Organization.location.isnot(None))
            stmt = stmt.where(
                func.ST_DWithin(Organization.location, reference_point_geog, radius_meters)
            )
            distance_expr = (
                func.ST_Distance(Organization.location, reference_point_geog) / 1000.0
            ).label("distance_km")
            stmt = stmt.add_columns(distance_expr)
            stmt = stmt.order_by(distance_expr)
        else:
            stmt = stmt.order_by(Organization.created_at.desc())

        stmt = stmt.offset(skip).limit(limit)

        if distance_expr is not None:
            records = db.execute(stmt).all()
            return [
                (
                    organization,
                    distance,
                    int(dogs_count or 0),
                    int(cats_count or 0),
                )
                for organization, dogs_count, cats_count, distance in records
            ]

        records = db.execute(stmt).all()
        return [
            (
                organization,
                None,
                int(dogs_count or 0),
                int(cats_count or 0),
            )
            for organization, dogs_count, cats_count in records
        ]
