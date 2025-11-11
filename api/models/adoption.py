from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

if TYPE_CHECKING:  # pragma: no cover
    from models.animal import Animal
    from models.organization import Organization


class Adoption(Base):
    """Registro histórico de adoções realizadas pela ONG."""

    __tablename__ = "adoptions"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        nullable=False,
    )
    organization_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
    )
    animal_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("animals.id", ondelete="CASCADE"),
        nullable=False,
    )
    adopter_name: Mapped[str] = mapped_column(String(255), nullable=False)
    adopter_document: Mapped[str | None] = mapped_column(String(32))
    adopter_email: Mapped[str | None] = mapped_column(String(255))
    adopter_phone: Mapped[str | None] = mapped_column(String(32))
    adoption_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    adoption_fee: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )
    contract_url: Mapped[str | None] = mapped_column(String(2048))
    volunteer_name: Mapped[str | None] = mapped_column(String(255))
    notes: Mapped[str | None] = mapped_column(Text())
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    closure_reason: Mapped[str | None] = mapped_column(Text())
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    organization: Mapped["Organization"] = relationship(
        "Organization",
        back_populates="adoptions",
    )
    animal: Mapped["Animal"] = relationship(
        "Animal",
        back_populates="adoptions",
    )

    @property
    def is_active(self) -> bool:
        return self.closed_at is None

    def __repr__(self) -> str:  # pragma: no cover - debugging helper
        return (
            f"Adoption(id={self.id!s}, animal_id={self.animal_id!s}, "
            f"adopter={self.adopter_name!r})"
        )


__all__ = ["Adoption"]
