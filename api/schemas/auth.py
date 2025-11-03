from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="E-mail cadastrado da ONG.")
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Senha de acesso.",
    )


class TokenResponse(BaseModel):
    access_token: str = Field(..., description="Token JWT que deve ser usado nas próximas requisições.")
    token_type: str = Field("bearer", description="Tipo de token emitido.")
    expires_in: int = Field(..., ge=1, description="Tempo de expiração do token em segundos.")


class LogoutResponse(BaseModel):
    message: str = Field(
        "Logout realizado com sucesso.",
        description="Mensagem de confirmação de logout.",
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Momento em que o logout foi processado.",
    )
