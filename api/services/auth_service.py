from dataclasses import dataclass
from datetime import timedelta
from typing import Tuple

from sqlalchemy.orm import Session

from core.config import get_settings
from core.security import create_access_token
from models.organization import Organization
from services.organization_service import (
    InactiveOrganizationError,
    InvalidCredentialsError,
    OrganizationService,
)


@dataclass(slots=True)
class AuthResult:
    access_token: str
    token_type: str
    expires_in: int
    organization: Organization


class AuthService:
    def __init__(self, organization_service: OrganizationService | None = None) -> None:
        self.organization_service = organization_service or OrganizationService()
        self.settings = get_settings()

    def login(self, db: Session, *, email: str, password: str) -> AuthResult:
        organization = self.organization_service.authenticate(
            db, email=email, password=password
        )

        expires_delta = timedelta(minutes=self.settings.access_token_expire_minutes)
        token = create_access_token(subject=organization.id, expires_delta=expires_delta)

        return AuthResult(
            access_token=token,
            token_type="bearer",
            expires_in=int(expires_delta.total_seconds()),
            organization=organization,
        )

    def logout(self) -> None:
        # JWT é stateless; manter método para extensões futuras (ex.: blacklist).
        return None
