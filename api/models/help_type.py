from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base
from models.association_tables import organization_help_types

if TYPE_CHECKING:  # pragma: no cover
    from models.organization import Organization


class HelpType(Base):
    """Tipos de ajuda disponíveis para as organizações."""

    __tablename__ = "help_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    label: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))

    organizations: Mapped[list["Organization"]] = relationship(
        "Organization",
        secondary=organization_help_types,
        back_populates="help_types",
    )
