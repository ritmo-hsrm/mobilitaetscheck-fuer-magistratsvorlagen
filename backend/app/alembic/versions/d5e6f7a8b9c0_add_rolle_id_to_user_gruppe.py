"""add rolle_id to user_gruppe

Revision ID: d5e6f7a8b9c0
Revises: c4d5e6f7a8b9
Create Date: 2026-03-20 00:00:00.000000
"""
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op

revision: str = "d5e6f7a8b9c0"
down_revision: Union[str, None] = "c4d5e6f7a8b9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "user_gruppe",
        sa.Column("rolle_id", sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        "fk_user_gruppe_rolle_id",
        "user_gruppe",
        "user_rolle",
        ["rolle_id"],
        ["id"],
        ondelete="SET NULL",
    )
    # Set all existing groups to the Verwaltung role
    conn = op.get_bind()
    verwaltung_id = conn.execute(
        sa.text("SELECT id FROM user_rolle WHERE name = 'Verwaltung' LIMIT 1")
    ).scalar()
    if verwaltung_id is not None:
        conn.execute(
            sa.text("UPDATE user_gruppe SET rolle_id = :rid WHERE rolle_id IS NULL"),
            {"rid": verwaltung_id},
        )


def downgrade() -> None:
    op.drop_constraint("fk_user_gruppe_rolle_id", "user_gruppe", type_="foreignkey")
    op.drop_column("user_gruppe", "rolle_id")
