from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import AnyUrl, BaseModel, Field, computed_field, field_validator

from schemas.expense_category import ExpenseCategoryRead


class ExpenseAttachmentBase(BaseModel):
    url: AnyUrl | str = Field(..., max_length=2048)
    file_name: str | None = Field(None, max_length=255)


class ExpenseAttachmentCreate(ExpenseAttachmentBase):
    pass


class ExpenseAttachmentRead(ExpenseAttachmentBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class ExpenseBase(BaseModel):
    category_id: UUID
    expense_date: date
    amount: Decimal = Field(..., gt=0, max_digits=12, decimal_places=2)
    description: str | None = Field(None, max_length=500)
    cost_center: str | None = Field(None, max_length=100)
    receipt_url: str | None = Field(None, max_length=2048)
    animal_id: UUID | None = None

    @field_validator("expense_date")
    @classmethod
    def _validate_date(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("A data da despesa não pode estar no futuro.")
        return value


class ExpenseCreate(ExpenseBase):
    attachments: list[ExpenseAttachmentCreate] = Field(default_factory=list)


class ExpenseRead(ExpenseBase):
    id: UUID
    organization_id: UUID
    category: ExpenseCategoryRead
    created_at: datetime
    updated_at: datetime
    attachments: list[ExpenseAttachmentRead] = Field(default_factory=list)

    class Config:
        from_attributes = True

    @computed_field
    @property
    def category_name(self) -> str:
        return self.category.name
