from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import AnyUrl, BaseModel, Field, field_validator


class AdoptionBase(BaseModel):
    animal_id: UUID
    adopter_name: str = Field(..., min_length=2, max_length=255)
    adopter_document: str | None = Field(None, max_length=32)
    adopter_email: str | None = Field(None, max_length=255)
    adopter_phone: str | None = Field(None, max_length=32)
    adoption_date: datetime | None = Field(
        default=None,
        description="Momento em que a adoção foi formalizada.",
    )
    adoption_fee: Decimal | None = Field(
        default=None,
        ge=0,
        description="Taxa cobrada no processo de adoção, quando aplicável.",
    )
    notes: str | None = Field(None, max_length=5_000)

    @field_validator("adoption_date")
    @classmethod
    def _validate_adoption_date(cls, value: datetime | None) -> datetime | None:
        if value and value > datetime.utcnow():
            raise ValueError("A data de adoção não pode estar no futuro.")
        return value


class AdoptionCreate(AdoptionBase):
    pass


class AdoptionClose(BaseModel):
    closed_at: datetime = Field(..., description="Momento em que a adoção foi encerrada.")
    closure_reason: str | None = Field(
        None,
        max_length=5_000,
        description="Justificativa opcional para encerramento/devolução.",
    )

    @field_validator("closed_at")
    @classmethod
    def _validate_closed_at(cls, value: datetime) -> datetime:
        if value > datetime.utcnow():
            raise ValueError("A data de encerramento não pode estar no futuro.")
        return value


class AdoptionRead(AdoptionBase):
    id: UUID
    organization_id: UUID
    closed_at: datetime | None = None
    closure_reason: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
