from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base
from models.association_tables import organization_help_types

if TYPE_CHECKING:  # pragma: no cover
    from models.animal import Animal
    from models.expense import Expense
    from models.expense_category import ExpenseCategory
    from models.help_type import HelpType


class Organization(Base):
    """Representa uma organização cadastrada na plataforma."""

    __tablename__ = "organizations"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    cnpj: Mapped[str] = mapped_column(String(18), unique=True, nullable=False)
    address: Mapped[str | None] = mapped_column(String(255))
    city: Mapped[str | None] = mapped_column(String(100))
    state: Mapped[str | None] = mapped_column(String(2))
    phone: Mapped[str | None] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    hashed_password: Mapped[str | None] = mapped_column(String(255))
    website: Mapped[str | None] = mapped_column(String(255))
    instagram: Mapped[str | None] = mapped_column(String(255))
    mission: Mapped[str | None] = mapped_column(Text())
    logo_url: Mapped[str | None] = mapped_column(String(255))
    accepts_terms: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    help_types: Mapped[list["HelpType"]] = relationship(
        "HelpType",
        secondary=organization_help_types,
        back_populates="organizations",
        lazy="joined",
    )
    animals: Mapped[list["Animal"]] = relationship(
        "Animal",
        back_populates="organization",
        cascade="all, delete-orphan",
    )
    expense_categories: Mapped[list["ExpenseCategory"]] = relationship(
        "ExpenseCategory",
        back_populates="organization",
        cascade="all, delete-orphan",
    )
    expenses: Mapped[list["Expense"]] = relationship(
        "Expense",
        back_populates="organization",
        cascade="all, delete-orphan",
    )
