from __future__ import annotations

from datetime import date, datetime
from typing import List
from uuid import UUID

from pydantic import AnyHttpUrl, BaseModel, Field, field_validator

from models.animal import (
    AnimalSex,
    AnimalSize,
    AnimalStatus,
    EnvironmentPreference,
    SociableTarget,
    TemperamentTrait,
)


class AnimalSpeciesBase(BaseModel):
    slug: str = Field(..., min_length=2, max_length=50)
    label: str = Field(..., min_length=2, max_length=100)
    description: str | None = Field(None, max_length=255)


class AnimalSpeciesRead(AnimalSpeciesBase):
    id: int

    class Config:
        from_attributes = True


class AnimalPhotoBase(BaseModel):
    url: AnyHttpUrl | str = Field(..., max_length=255)
    position: int | None = Field(
        None,
        ge=0,
        description="Ordem em que a foto deve aparecer.",
    )


class AnimalPhotoCreate(AnimalPhotoBase):
    pass


class AnimalPhotoRead(AnimalPhotoBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class AnimalBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    sex: AnimalSex = AnimalSex.unknown
    age_years: int | None = Field(None, ge=0, le=50)
    weight_kg: float | None = Field(None, ge=0, le=200)
    size: AnimalSize = AnimalSize.unknown
    temperament_traits: list[TemperamentTrait] = Field(
        default_factory=list,
        description="Etiquetas exibidas como chips para temperamento.",
    )
    environment_preferences: list[EnvironmentPreference] = Field(
        default_factory=list,
        description="Ambientes recomendados (ex: apartamento, casa com quintal).",
    )
    sociable_with: list[SociableTarget] = Field(
        default_factory=list,
        description="Com quem o pet convive bem (ex: crianças, gatos).",
    )
    vaccinated: bool = False
    neutered: bool = False
    dewormed: bool = False
    rescue_date: date | None = None
    microchip: str | None = Field(None, max_length=50)
    description: str | None = None
    adoption_requirements: str | None = None
    status: AnimalStatus = AnimalStatus.available

    @field_validator("rescue_date")
    @classmethod
    def _validate_rescue_date(cls, value: date | None) -> date | None:
        if value and value > date.today():
            raise ValueError("A data de resgate não pode estar no futuro.")
        return value


class AnimalCreate(AnimalBase):
    species_id: int = Field(..., ge=1)
    photos: List[AnimalPhotoCreate] = Field(default_factory=list)


class AnimalRead(AnimalBase):
    id: UUID
    organization_id: UUID
    species: AnimalSpeciesRead
    created_at: datetime
    updated_at: datetime
    photos: list[AnimalPhotoRead] = Field(default_factory=list)

    class Config:
        from_attributes = True


class AnimalOrganizationSummary(BaseModel):
    id: UUID
    name: str = Field(..., min_length=1, max_length=255)
    city: str | None = Field(None, max_length=100)
    state: str | None = Field(None, min_length=2, max_length=2)
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)
    logo_url: str | None = Field(None, max_length=255)

    class Config:
        from_attributes = True


class AnimalPublicRead(AnimalRead):
    distance_km: float = Field(
        ...,
        ge=0,
        description="Distância aproximada em quilômetros até as coordenadas informadas.",
    )
    organization: AnimalOrganizationSummary


class AnimalListItemRead(BaseModel):
    id: UUID
    name: str = Field(..., min_length=1, max_length=255)
    status: AnimalStatus
    species: AnimalSpeciesRead
    photo_url: AnyHttpUrl | str | None = Field(
        None,
        description="URL da principal foto cadastrada para o animal.",
    )


class AnimalCharacteristicOption(BaseModel):
    value: str
    label: str


class AnimalCharacteristicsRead(BaseModel):
    temperament_traits: list[AnimalCharacteristicOption]
    environment_preferences: list[AnimalCharacteristicOption]
    sociable_with: list[AnimalCharacteristicOption]
