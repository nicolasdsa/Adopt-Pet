"""create organizations table

Revision ID: 0001_create_organizations_table
Revises:
Create Date: 2025-10-28 00:00:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import table, column

# revision identifiers, used by Alembic.
revision = "0001_create_organizations"
down_revision = None
branch_labels = None
depends_on = None

help_types_data = [
    {"id": 1, "key": "donation", "label": "Doação"},
    {"id": 2, "key": "volunteering", "label": "Voluntariado"},
    {"id": 3, "key": "temporary_home", "label": "Lar Temporário"},
]


def upgrade() -> None:
    op.create_table(
        "help_types",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("key", sa.String(length=50), nullable=False, unique=True),
        sa.Column("label", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
    )

    op.create_table(
        "organizations",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("cnpj", sa.String(length=18), nullable=False, unique=True),
        sa.Column("address", sa.String(length=255), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("state", sa.String(length=2), nullable=True),
        sa.Column("phone", sa.String(length=20), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("website", sa.String(length=255), nullable=True),
        sa.Column("instagram", sa.String(length=255), nullable=True),
        sa.Column("mission", sa.Text(), nullable=True),
        sa.Column("logo_url", sa.String(length=255), nullable=True),
        sa.Column(
            "accepts_terms",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
            server_onupdate=sa.func.now(),
        ),
        sa.Column("hashed_password", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )

    op.create_index("ix_organizations_id", "organizations", ["id"])
    op.create_index("ix_organizations_email", "organizations", ["email"])

    op.create_table(
        "organization_help_types",
        sa.Column(
            "organization_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("organizations.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "help_type_id",
            sa.Integer(),
            sa.ForeignKey("help_types.id", ondelete="CASCADE"),
            primary_key=True,
        ),
    )

    help_types_table = table(
        "help_types",
        column("id", sa.Integer()),
        column("key", sa.String(length=50)),
        column("label", sa.String(length=100)),
    )
    op.bulk_insert(help_types_table, help_types_data)


def downgrade() -> None:
    op.drop_table("organization_help_types")
    op.drop_index("ix_organizations_email", table_name="organizations")
    op.drop_index("ix_organizations_id", table_name="organizations")
    op.drop_table("organizations")
    op.drop_table("help_types")