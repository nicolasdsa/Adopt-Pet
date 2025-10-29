from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.orm import Session, joinedload

from models.organization import Organization


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
