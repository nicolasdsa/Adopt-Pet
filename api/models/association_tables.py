from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from db.base import Base

organization_help_types = Table(
    "organization_help_types",
    Base.metadata,
    Column(
        "organization_id",
        PGUUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "help_type_id",
        Integer,
        ForeignKey("help_types.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

__all__ = ["organization_help_types"]
