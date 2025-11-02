"""create animals and animal_photos tables

Revision ID: 0002_create_animals
Revises: 0001_create_organizations
Create Date: 2025-10-28 00:10:00
"""

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import column, table

from alembic import op

# revision identifiers, used by Alembic.
revision = "0002_create_animals"
down_revision = "0001_create_organizations"
branch_labels = None
depends_on = None

animal_sex_enum = sa.Enum(
    "male",
    "female",
    "unknown",
    name="animal_sex",
)

animal_size_enum = sa.Enum(
    "small",
    "medium",
    "large",
    "unknown",
    name="animal_size",
)

animal_status_enum = sa.Enum(
    "available", "reserved", "adopted", "draft", name="animal_status"
)

animal_species_seed = [
    {"id": 1, "slug": "dog", "label": "Cachorro"},
    {"id": 2, "slug": "cat", "label": "Gato"},
]


def upgrade() -> None:
    bind = op.get_bind()
    animal_sex_enum.create(bind, checkfirst=True)
    animal_size_enum.create(bind, checkfirst=True)
    animal_status_enum.create(bind, checkfirst=True)

    op.create_table(
        "animal_species",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("slug", sa.String(length=50), nullable=False, unique=True),
        sa.Column("label", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
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
    )

    op.create_table(
        "animals",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "organization_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("organizations.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column(
            "species_id",
            sa.Integer(),
            sa.ForeignKey("animal_species.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("sex", animal_sex_enum, nullable=False, server_default="unknown"),
        sa.Column("age_years", sa.Integer(), nullable=True),
        sa.Column("weight_kg", sa.Float(), nullable=True),
        sa.Column("size", animal_size_enum, nullable=False, server_default="unknown"),
        sa.Column("temperament", sa.String(length=255), nullable=True),
        sa.Column(
            "vaccinated",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column(
            "neutered",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column(
            "dewormed",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column("rescue_date", sa.Date(), nullable=True),
        sa.Column("microchip", sa.String(length=50), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("adoption_requirements", sa.Text(), nullable=True),
        sa.Column(
            "status",
            animal_status_enum,
            nullable=False,
            server_default="available",
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
    )
    op.create_index(
        "ix_animals_organization_id",
        "animals",
        ["organization_id"],
    )
    op.create_index("ix_animals_species_id", "animals", ["species_id"])
    op.create_index("ix_animals_status", "animals", ["status"])

    op.create_table(
        "animal_photos",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "animal_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("animals.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("url", sa.String(length=255), nullable=False),
        sa.Column("position", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )
    op.create_index(
        "ix_animal_photos_animal_id",
        "animal_photos",
        ["animal_id"],
    )

    species_table = table(
        "animal_species",
        column("id", sa.Integer()),
        column("slug", sa.String(length=50)),
        column("label", sa.String(length=100)),
    )
    op.bulk_insert(species_table, animal_species_seed)


def downgrade() -> None:
    op.drop_index("ix_animal_photos_animal_id", table_name="animal_photos")
    op.drop_table("animal_photos")

    op.drop_index("ix_animals_status", table_name="animals")
    op.drop_index("ix_animals_organization_id", table_name="animals")
    op.drop_index("ix_animals_species_id", table_name="animals")
    op.drop_table("animals")
    op.drop_table("animal_species")

    bind = op.get_bind()
    animal_status_enum.drop(bind, checkfirst=True)
    animal_size_enum.drop(bind, checkfirst=True)
    animal_sex_enum.drop(bind, checkfirst=True)
