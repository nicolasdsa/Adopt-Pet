from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID

from sqlalchemy.orm import Session

from models.expense import Expense
from models.expense_attachment import ExpenseAttachment
from models.organization import Organization
from repositories.animal_repository import AnimalRepository
from repositories.expense_category_repository import ExpenseCategoryRepository
from repositories.expense_repository import ExpenseRepository
from schemas.expense import ExpenseCreate


class ExpenseCategoryUnavailableError(Exception):
    """Raised when the category cannot be used by the organization."""


class ExpenseAnimalNotFoundError(Exception):
    """Raised when the optional animal is not found or does not belong to the organization."""


class ExpenseNotFoundError(Exception):
    """Raised when an expense cannot be located for the organization."""


@dataclass(slots=True)
class ExpenseService:
    """Regras de negócio relacionadas às despesas."""

    expense_repository: ExpenseRepository = ExpenseRepository()
    category_repository: ExpenseCategoryRepository = ExpenseCategoryRepository()
    animal_repository: AnimalRepository = AnimalRepository()

    def create_expense(
        self, db: Session, organization: Organization, payload: ExpenseCreate
    ) -> Expense:
        category = self.category_repository.get_by_id(db, payload.category_id)
        if (
            category is None
            or category.organization_id not in (None, organization.id)
        ):
            raise ExpenseCategoryUnavailableError

        animal = None
        if payload.animal_id is not None:
            animal = self.animal_repository.get_by_id(db, payload.animal_id)
            if animal is None or animal.organization_id != organization.id:
                raise ExpenseAnimalNotFoundError

        expense = Expense(
            organization_id=organization.id,
            category_id=payload.category_id,
            animal_id=payload.animal_id,
            description=payload.description,
            amount=payload.amount,
            expense_date=payload.expense_date,
            cost_center=payload.cost_center,
            receipt_url=payload.receipt_url,
        )
        if animal is not None:
            expense.animal = animal
        expense.category = category
        expense.attachments = [
            ExpenseAttachment(url=str(attachment.url), file_name=attachment.file_name)
            for attachment in payload.attachments
        ]

        self.expense_repository.add(db, expense)
        try:
            db.commit()
        except Exception:
            db.rollback()
            raise

        db.refresh(expense)
        return expense

    def list_expenses(
        self,
        db: Session,
        organization: Organization,
        *,
        skip: int = 0,
        limit: int = 50,
        category_id: UUID | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[Expense]:
        return self.expense_repository.list_by_organization(
            db,
            organization.id,
            skip=skip,
            limit=limit,
            category_id=category_id,
            start_date=start_date,
            end_date=end_date,
        )

    def get_expense(
        self, db: Session, organization: Organization, expense_id: UUID
    ) -> Expense:
        expense = self.expense_repository.get_by_id_for_organization(
            db, expense_id, organization.id
        )
        if expense is None:
            raise ExpenseNotFoundError
        return expense
