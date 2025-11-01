from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.security import InvalidTokenError, decode_token
from db.session import get_db
from models.organization import Organization
from repositories.organization_repository import OrganizationRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/ongs/login")
organization_repository = OrganizationRepository()


def get_current_organization(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Organization:
    """Dependência planejada para proteger rotas com autenticação JWT."""
    try:
        payload = decode_token(token)
        organization_id = UUID(payload.get("sub", ""))
    except (InvalidTokenError, ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado.",
        )

    organization = organization_repository.get_by_id(db, organization_id)
    if organization is None or not organization.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autenticação necessária.",
        )
    return organization
