"""create expense categories and expenses tables

Revision ID: 0003_create_expenses
Revises: 0002_create_animals
Create Date: 2025-10-28 01:00:00
"""

from uuid import uuid4

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import column, table

# revision identifiers, used by Alembic.
revision = "0003_create_expenses"
down_revision = "0002_create_animals"
branch_labels = None
depends_on = None

expense_categories = table(
    "expense_categories",
    column("id", postgresql.UUID(as_uuid=True)),
    column("key", sa.String(length=50)),
    column("name", sa.String(length=100)),
    column("icon", sa.String(length=100)),
)

default_categories = [
    {"id": uuid4(), "key": "food", "name": "Alimentação", "icon": "utensils"},
    {"id": uuid4(), "key": "medical", "name": "Despesas Médicas", "icon": "stethoscope"},
    {"id": uuid4(), "key": "other", "name": "Outros", "icon": "tag"},
]


def upgrade() -> None:
    op.create_table(
        "expense_categories",
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
            nullable=True,
        ),
        sa.Column("key", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("icon", sa.String(length=100), nullable=False),
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
        sa.CheckConstraint("char_length(key) >= 2", name="ck_expense_categories_key"),
        sa.CheckConstraint("char_length(name) >= 2", name="ck_expense_categories_name"),
        sa.CheckConstraint("char_length(icon) >= 1", name="ck_expense_categories_icon"),
    )
    op.create_index(
        "ix_expense_categories_organization_id",
        "expense_categories",
        ["organization_id"],
    )
    op.create_index(
        "uq_expense_categories_org_key",
        "expense_categories",
        ["organization_id", "key"],
        unique=True,
    )
    op.create_index(
        "uq_expense_categories_key_global",
        "expense_categories",
        ["key"],
        unique=True,
        postgresql_where=sa.text("organization_id IS NULL"),
    )

    op.create_table(
        "expenses",
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
        sa.Column(
            "category_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "animal_id",
            postgresql.UUID(as_uuid=True),
            nullable=True,
        ),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "amount",
            sa.Numeric(12, 2),
            nullable=False,
        ),
        sa.Column("expense_date", sa.Date(), nullable=False),
        sa.Column("cost_center", sa.String(length=100), nullable=True),
        sa.Column("receipt_url", sa.String(length=2048), nullable=True),
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
        sa.CheckConstraint("amount >= 0", name="ck_expenses_amount_positive"),
    )
    op.create_index(
        "ix_expenses_organization_id",
        "expenses",
        ["organization_id"],
    )
    op.create_index(
        "ix_expenses_category_id",
        "expenses",
        ["category_id"],
    )
    op.create_index(
        "ix_expenses_expense_date",
        "expenses",
        ["expense_date"],
    )

    op.create_table(
        "expense_attachments",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "expense_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("expenses.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("file_name", sa.String(length=255), nullable=True),
        sa.Column("url", sa.String(length=2048), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )
    op.create_index(
        "ix_expense_attachments_expense_id",
        "expense_attachments",
        ["expense_id"],
    )

    op.create_unique_constraint(
        "uq_animals_id_organization_id",
        "animals",
        ["id", "organization_id"],
    )
    op.create_foreign_key(
        "fk_expenses_category",
        "expenses",
        "expense_categories",
        ["category_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.create_foreign_key(
        "fk_expenses_animal_same_org",
        "expenses",
        "animals",
        ["animal_id", "organization_id"],
        ["id", "organization_id"],
        deferrable=True,
        initially="IMMEDIATE",
    )

    op.execute(
        sa.text(
            """
CREATE OR REPLACE FUNCTION check_expense_relations()
RETURNS trigger AS $$
BEGIN
    IF NEW.category_id IS NOT NULL THEN
        IF NOT EXISTS (
            SELECT 1
            FROM expense_categories ec
            WHERE ec.id = NEW.category_id
              AND (ec.organization_id IS NULL OR ec.organization_id = NEW.organization_id)
        ) THEN
            RAISE EXCEPTION 'Categoria de despesa inválida para a organização.' USING ERRCODE = '23514';
        END IF;
    END IF;

    IF NEW.animal_id IS NOT NULL THEN
        IF NOT EXISTS (
            SELECT 1
            FROM animals a
            WHERE a.id = NEW.animal_id
              AND a.organization_id = NEW.organization_id
        ) THEN
            RAISE EXCEPTION 'Animal inválido para a organização.' USING ERRCODE = '23514';
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""
        )
    )
    op.execute(
        """
CREATE TRIGGER trg_expenses_validate_relations
BEFORE INSERT OR UPDATE ON expenses
FOR EACH ROW EXECUTE FUNCTION check_expense_relations();
"""
    )

    op.bulk_insert(expense_categories, default_categories)


def downgrade() -> None:
    op.execute(
        "DROP TRIGGER IF EXISTS trg_expenses_validate_relations ON expenses"
    )
    op.execute("DROP FUNCTION IF EXISTS check_expense_relations")

    op.drop_constraint(
        "fk_expenses_animal_same_org",
        "expenses",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_expenses_category",
        "expenses",
        type_="foreignkey",
    )
    op.drop_index(
        "ix_expense_attachments_expense_id",
        table_name="expense_attachments",
    )
    op.drop_table("expense_attachments")

    op.drop_index("ix_expenses_expense_date", table_name="expenses")
    op.drop_index("ix_expenses_category_id", table_name="expenses")
    op.drop_index("ix_expenses_organization_id", table_name="expenses")
    op.drop_table("expenses")

    op.drop_constraint(
        "uq_animals_id_organization_id",
        "animals",
        type_="unique",
    )

    op.drop_index("uq_expense_categories_key_global", table_name="expense_categories")
    op.drop_index("uq_expense_categories_org_key", table_name="expense_categories")
    op.drop_index(
        "ix_expense_categories_organization_id",
        table_name="expense_categories",
    )
    op.drop_table("expense_categories")
