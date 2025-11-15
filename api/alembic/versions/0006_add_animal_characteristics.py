"""add behavior tags to animals

Revision ID: 0006_add_animal_characteristics
Revises: 0005_create_adoptions
Create Date: 2025-10-28 00:30:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0006_add_animal_characteristics"
down_revision = "0005_create_adoptions"
branch_labels = None
depends_on = None

TEMPERAMENT_VALUES = [
    "docile",
    "playful",
    "calm",
    "shy",
    "protective",
    "energetic",
]
ENVIRONMENT_VALUES = [
    "apartment",
    "house_with_yard",
    "farm_or_ranch",
    "active_family",
]
SOCIABLE_VALUES = [
    "dogs",
    "cats",
    "children",
    "unknown_people",
    "elderly",
    "other_pets",
]


def _create_enum(name: str, values: list[str]) -> None:
    values_sql = ", ".join(f"'{value}'" for value in values)
    op.execute(
        sa.text(
            f"""
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = '{name}') THEN
        CREATE TYPE {name} AS ENUM ({values_sql});
    END IF;
END
$$;
"""
        )
    )


def _drop_enum(name: str) -> None:
    op.execute(sa.text(f"DROP TYPE IF EXISTS {name}"))


def upgrade() -> None:
    _create_enum("temperament_trait", TEMPERAMENT_VALUES)
    _create_enum("environment_preference", ENVIRONMENT_VALUES)
    _create_enum("sociable_target", SOCIABLE_VALUES)

    op.add_column(
        "animals",
        sa.Column(
            "temperament_traits",
            postgresql.ARRAY(
                sa.Enum(
                    *TEMPERAMENT_VALUES,
                    name="temperament_trait",
                    create_type=False,
                )
            ),
            nullable=False,
            server_default=sa.text("'{}'::temperament_trait[]"),
        ),
    )
    op.add_column(
        "animals",
        sa.Column(
            "environment_preferences",
            postgresql.ARRAY(
                sa.Enum(
                    *ENVIRONMENT_VALUES,
                    name="environment_preference",
                    create_type=False,
                )
            ),
            nullable=False,
            server_default=sa.text("'{}'::environment_preference[]"),
        ),
    )
    op.add_column(
        "animals",
        sa.Column(
            "sociable_with",
            postgresql.ARRAY(
                sa.Enum(
                    *SOCIABLE_VALUES,
                    name="sociable_target",
                    create_type=False,
                )
            ),
            nullable=False,
            server_default=sa.text("'{}'::sociable_target[]"),
        ),
    )

    op.drop_column("animals", "temperament")

    op.alter_column("animals", "temperament_traits", server_default=None)
    op.alter_column("animals", "environment_preferences", server_default=None)
    op.alter_column("animals", "sociable_with", server_default=None)


def downgrade() -> None:
    op.add_column(
        "animals",
        sa.Column("temperament", sa.String(length=255), nullable=True),
    )
    op.drop_column("animals", "sociable_with")
    op.drop_column("animals", "environment_preferences")
    op.drop_column("animals", "temperament_traits")

    _drop_enum("sociable_target")
    _drop_enum("environment_preference")
    _drop_enum("temperament_trait")
