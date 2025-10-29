from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.help_type import HelpType
from models.organization import Organization
from repositories.help_type_repository import HelpTypeRepository
from repositories.organization_repository import OrganizationRepository
from schemas.organization import OrganizationCreate


class OrganizationNotFoundError(Exception):
    """Raised when an organization is not found."""


class DuplicateCNPJError(Exception):
    """Raised when attempting to register a duplicated CNPJ."""


@dataclass(slots=True)
class HelpTypeNotFoundError(Exception):
    missing_keys: set[str]

    def __str__(self) -> str:  # pragma: no cover - trivial
        keys = ", ".join(sorted(self.missing_keys))
        return f"Tipos de ajuda não encontrados: {keys}."


class OrganizationService:
    """Regras de negócio para o domínio de organizações."""

    def __init__(
        self,
        organization_repository: OrganizationRepository | None = None,
        help_type_repository: HelpTypeRepository | None = None,
    ) -> None:
        self.organization_repository = organization_repository or OrganizationRepository()
        self.help_type_repository = help_type_repository or HelpTypeRepository()

    def create_organization(
        self, db: Session, payload: OrganizationCreate
    ) -> Organization:
        data = payload.model_dump(exclude={"help_types"}, exclude_none=True)

        keys = [help_type.value for help_type in payload.help_types]
        help_types = self._get_help_types_by_keys(db, keys)

        organization = Organization(**data)
        organization.help_types = [help_types[key] for key in keys]

        self.organization_repository.add(db, organization)

        try:
            db.commit()
        except IntegrityError as exc:
            db.rollback()
            raise DuplicateCNPJError from exc

        db.refresh(organization)
        return organization

    def list_organizations(
        self, db: Session, *, skip: int = 0, limit: int = 50
    ) -> list[Organization]:
        return self.organization_repository.list(db, skip=skip, limit=limit)

    def get_organization(self, db: Session, organization_id: UUID) -> Organization:
        organization = self.organization_repository.get_by_id(db, organization_id)
        if organization is None:
            raise OrganizationNotFoundError
        return organization

    def _get_help_types_by_keys(
        self, db: Session, keys: Iterable[str]
    ) -> dict[str, HelpType]:
        help_types = self.help_type_repository.get_by_keys(db, keys)
        help_types_by_key = {help_type.key: help_type for help_type in help_types}
        missing = set(keys) - set(help_types_by_key)
        if missing:
            raise HelpTypeNotFoundError(missing)
        return help_types_by_key
