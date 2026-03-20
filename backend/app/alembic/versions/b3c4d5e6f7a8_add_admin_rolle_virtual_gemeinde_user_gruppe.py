"""add admin rolle, virtual gemeinde, user_gruppe

Revision ID: b3c4d5e6f7a8
Revises: f6a7b8c9d0e1
Create Date: 2026-03-19 00:00:00.000000
"""
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "b3c4d5e6f7a8"
down_revision: Union[str, None] = "f6a7b8c9d0e1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

VIRTUAL_GEMEINDE_NAME = "Systemadministration"
ADMIN_ROLLE_NAME = "Admin"


def upgrade() -> None:
    conn = op.get_bind()
    existing_admin = conn.execute(
        sa.text("SELECT id FROM user_rolle WHERE name = :name").bindparams(name=ADMIN_ROLLE_NAME)
    ).scalar()
    if existing_admin is None:
        conn.execute(
            sa.text("INSERT INTO user_rolle (name) VALUES (:name)").bindparams(name=ADMIN_ROLLE_NAME)
        )

    existing_gemeinde = conn.execute(
        sa.text("SELECT id FROM gemeinde WHERE name = :name").bindparams(name=VIRTUAL_GEMEINDE_NAME)
    ).scalar()
    if existing_gemeinde is None:
        conn.execute(
            sa.text("INSERT INTO gemeinde (name) VALUES (:name)").bindparams(name=VIRTUAL_GEMEINDE_NAME)
        )

    op.create_table(
        "user_gruppe",
        sa.Column("id", sa.Integer(), nullable=False, comment="Gruppe ID"),
        sa.Column("name", sa.String(), nullable=False, comment="Name der Gruppe"),
        sa.Column("gemeinde_id", sa.Integer(), nullable=False, comment="Gemeinde ID"),
        sa.ForeignKeyConstraint(["gemeinde_id"], ["gemeinde.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_gruppe_id"), "user_gruppe", ["id"], unique=True)

    op.add_column(
        "user",
        sa.Column("gruppe_id", sa.Integer(), nullable=True, comment="Gruppe des Benutzers"),
    )
    op.create_foreign_key(None, "user", "user_gruppe", ["gruppe_id"], ["id"], ondelete="SET NULL")


def downgrade() -> None:
    op.drop_constraint(None, "user", type_="foreignkey")
    op.drop_column("user", "gruppe_id")
    op.drop_index(op.f("ix_user_gruppe_id"), table_name="user_gruppe")
    op.drop_table("user_gruppe")
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM user_rolle WHERE name = :name").bindparams(name=ADMIN_ROLLE_NAME))
    conn.execute(sa.text("DELETE FROM gemeinde WHERE name = :name").bindparams(name=VIRTUAL_GEMEINDE_NAME))
