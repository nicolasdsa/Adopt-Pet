from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum as SAEnum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

if TYPE_CHECKING:  # pragma: no cover
    from models.animal_photo import AnimalPhoto
    from models.animal_species import AnimalSpecies
    from models.organization import Organization


class AnimalSex(str, Enum):
    male = "male"
    female = "female"
    unknown = "unknown"


class AnimalSize(str, Enum):
    small = "small"
    medium = "medium"
    large = "large"
    unknown = "unknown"


class AnimalStatus(str, Enum):
    available = "available"
    reserved = "reserved"
    adopted = "adopted"
    draft = "draft"


class Animal(Base):
    """Representa um animal disponível para adoção."""

    __tablename__ = "animals"

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
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    species_id: Mapped[int] = mapped_column(
        ForeignKey("animal_species.id", ondelete="RESTRICT"),
        nullable=False,
    )
    sex: Mapped[AnimalSex] = mapped_column(
        SAEnum(AnimalSex, name="animal_sex"),
        nullable=False,
        default=AnimalSex.unknown,
    )
    age_years: Mapped[int | None] = mapped_column(Integer())
    weight_kg: Mapped[float | None] = mapped_column(Float())
    size: Mapped[AnimalSize] = mapped_column(
        SAEnum(AnimalSize, name="animal_size"),
        nullable=False,
        default=AnimalSize.unknown,
    )
    temperament: Mapped[str | None] = mapped_column(String(255))
    vaccinated: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=func.false()
    )
    neutered: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=func.false()
    )
    dewormed: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=func.false()
    )
    rescue_date: Mapped[date | None] = mapped_column(Date())
    microchip: Mapped[str | None] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(Text())
    adoption_requirements: Mapped[str | None] = mapped_column(Text())
    status: Mapped[AnimalStatus] = mapped_column(
        SAEnum(AnimalStatus, name="animal_status"),
        nullable=False,
        default=AnimalStatus.available,
    )
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
        back_populates="animals",
    )
    species: Mapped["AnimalSpecies"] = relationship(
        "AnimalSpecies",
        back_populates="animals",
        lazy="joined",
    )
    photos: Mapped[list["AnimalPhoto"]] = relationship(
        "AnimalPhoto",
        back_populates="animal",
        cascade="all, delete-orphan",
        order_by="AnimalPhoto.position",
    )

    def __repr__(self) -> str:  # pragma: no cover - debugging helper
        return f"Animal(id={self.id!s}, name={self.name!r})"


__all__ = ["Animal", "AnimalSex", "AnimalSize", "AnimalStatus"]
