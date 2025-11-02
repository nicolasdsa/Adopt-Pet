from __future__ import annotations
from __future__ import annotations

from datetime import date, datetime
from typing import List
from uuid import UUID

from pydantic import AnyHttpUrl, BaseModel, Field, field_validator

from models.animal import AnimalSex, AnimalSize, AnimalStatus


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
    temperament: str | None = Field(None, max_length=255)
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
