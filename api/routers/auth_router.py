from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from controllers.auth_controller import login, logout
from db.session import get_db
from schemas.auth import LoginRequest, LogoutResponse, TokenResponse

router = APIRouter(prefix="/ongs", tags=["Auth"])


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Realizar login da ONG",
)
def login_organization(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    return login(payload, db)


@router.post(
    "/logout",
    response_model=LogoutResponse,
    status_code=status.HTTP_200_OK,
    summary="Realizar logout da ONG",
)
def logout_organization() -> LogoutResponse:
    return logout()
