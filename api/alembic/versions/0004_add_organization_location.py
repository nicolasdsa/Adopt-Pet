"""add geographic fields to organizations

Revision ID: 0004_add_organization_location
Revises: 0003_create_expenses
Create Date: 2025-10-28 02:00:00
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0004_add_organization_location"
down_revision = "0003_create_expenses"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    op.add_column(
        "organizations",
        sa.Column("latitude", sa.Numeric(9, 6), nullable=True),
    )
    op.add_column(
        "organizations",
        sa.Column("longitude", sa.Numeric(9, 6), nullable=True),
    )
    op.create_check_constraint(
        "ck_organizations_latitude_range",
        "organizations",
        "latitude BETWEEN -90 AND 90",
    )
    op.create_check_constraint(
        "ck_organizations_longitude_range",
        "organizations",
        "longitude BETWEEN -180 AND 180",
    )

    op.execute(
        "ALTER TABLE organizations ADD COLUMN location geography(Point, 4326)"
    )
    op.create_index(
        "ix_organizations_location",
        "organizations",
        ["location"],
        postgresql_using="gist",
    )
    op.execute(
        """
        UPDATE organizations
        SET location = ST_SetSRID(
            ST_MakePoint(longitude::double precision, latitude::double precision),
            4326
        )
        WHERE latitude IS NOT NULL AND longitude IS NOT NULL;
        """
    )


def downgrade() -> None:
    op.drop_index("ix_organizations_location", table_name="organizations")
    op.execute("ALTER TABLE organizations DROP COLUMN IF EXISTS location")
    op.drop_constraint(
        "ck_organizations_longitude_range",
        "organizations",
        type_="check",
    )
    op.drop_constraint(
        "ck_organizations_latitude_range",
        "organizations",
        type_="check",
    )
    op.drop_column("organizations", "longitude")
    op.drop_column("organizations", "latitude")
    op.execute("DROP EXTENSION IF EXISTS postgis")
