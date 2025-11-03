from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import AnyUrl, BaseModel, EmailStr, Field, model_validator


class HelpType(str, Enum):
    donation = "donation"
    volunteering = "volunteering"
    temporary_home = "temporary_home"


class OrganizationBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    cnpj: str = Field(..., min_length=14, max_length=18)
    address: str | None = Field(None, max_length=255)
    city: str | None = Field(None, max_length=100)
    state: str | None = Field(None, min_length=2, max_length=2)
    phone: str | None = Field(None, max_length=20)
    email: EmailStr
    website: AnyUrl | None = None
    instagram: str | None = Field(
        None, max_length=255, description="Perfil ou URL do Instagram."
    )
    mission: str | None = None
    help_types: list[HelpType] = Field(default_factory=list)
    logo_url: str | None = Field(
        None, max_length=255, description="Caminho ou URL do logo."
    )
    accepts_terms: bool = Field(False, description="Confirmação de aceite de termos.")
    latitude: float | None = Field(
        None,
        ge=-90,
        le=90,
        description="Latitude em graus decimais (WGS84).",
    )
    longitude: float | None = Field(
        None,
        ge=-180,
        le=180,
        description="Longitude em graus decimais (WGS84).",
    )


class OrganizationCreate(OrganizationBase):
    email: EmailStr
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Senha utilizada para autenticação da ONG.",
    )
    accepts_terms: bool = Field(
        True,
        description="O campo deve ser verdadeiro para completar o cadastro.",
    )

    @model_validator(mode="after")
    def _validate_terms(cls, model: "OrganizationCreate") -> "OrganizationCreate":
        if not model.accepts_terms:
            raise ValueError("Os termos de uso precisam ser aceitos.")
        return model


class OrganizationRead(OrganizationBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrganizationSearchRead(OrganizationRead):
    distance_km: float | None = Field(
        None,
        ge=0,
        description="Distância aproximada em quilômetros até a coordenada consultada.",
    )
    dogs_count: int = Field(
        0,
        ge=0,
        description="Quantidade de cães cadastrados pela ONG.",
    )
    cats_count: int = Field(
        0,
        ge=0,
        description="Quantidade de gatos cadastrados pela ONG.",
    )
