from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from schemas.auth import LoginRequest, LogoutResponse, TokenResponse
from services.auth_service import AuthResult, AuthService
from services.organization_service import (
    InactiveOrganizationError,
    InvalidCredentialsError,
)

auth_service = AuthService()


def login(payload: LoginRequest, db: Session) -> TokenResponse:
    try:
        result: AuthResult = auth_service.login(
            db, email=payload.email, password=payload.password
        )
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas.",
        )
    except InactiveOrganizationError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ONG inativa.",
        )

    return TokenResponse(
        access_token=result.access_token,
        token_type=result.token_type,
        expires_in=result.expires_in,
    )


def logout() -> LogoutResponse:
    auth_service.logout()
    return LogoutResponse()
