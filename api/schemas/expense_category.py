from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field


class ExpenseCategoryBase(BaseModel):
    key: str = Field(
        ...,
        min_length=2,
        max_length=50,
        pattern=r"^[a-z0-9-]+$",
        description="Identificador estável da categoria (slug).",
    )
    name: str = Field(..., min_length=2, max_length=100)
    icon: str = Field(..., min_length=1, max_length=100)


class ExpenseCategoryCreate(ExpenseCategoryBase):
    pass


class ExpenseCategoryRead(ExpenseCategoryBase):
    id: UUID
    is_global: bool

    class Config:
        from_attributes = True
