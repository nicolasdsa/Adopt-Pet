"""create adoptions table

Revision ID: 0005_create_adoptions
Revises: 0004_add_organization_location
Create Date: 2025-10-28 00:20:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0005_create_adoptions"
down_revision = "0004_add_organization_location"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "adoptions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("animal_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("animals.id", ondelete="CASCADE"), nullable=False),
        sa.Column("adopter_name", sa.String(255), nullable=False),
        sa.Column("adopter_document", sa.String(32)),
        sa.Column("adopter_email", sa.String(255)),
        sa.Column("adopter_phone", sa.String(32)),
        sa.Column("adoption_date", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("volunteer_name", sa.String(255)),
        sa.Column("notes", sa.Text()),
        sa.Column("closed_at", sa.DateTime(timezone=True)),
        sa.Column("closure_reason", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_index("ix_adoptions_organization_id", "adoptions", ["organization_id"])
    op.create_index("ix_adoptions_adoption_date", "adoptions", ["adoption_date"])

    # Índice único parcial (1 adoção ativa por animal)
    op.create_index(
        "uq_adoptions_active_animal",
        "adoptions",
        ["animal_id"],
        unique=True,
        postgresql_where=sa.text("closed_at IS NULL"),
    )

    # Consistência temporal
    op.create_check_constraint(
        "chk_closed_after_adoption",
        "adoptions",
        sa.text("closed_at IS NULL OR closed_at >= adoption_date"),
    )

def downgrade() -> None:
    op.drop_constraint("chk_closed_after_adoption", "adoptions", type_="check")
    op.drop_index("uq_adoptions_active_animal", table_name="adoptions")
    op.drop_index("ix_adoptions_adoption_date", table_name="adoptions")
    op.drop_index("ix_adoptions_organization_id", table_name="adoptions")
    op.drop_table("adoptions")