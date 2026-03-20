"""add standard_ziel_set_id to gemeinde

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-03-18 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c3d4e5f6a7b8"
down_revision: Union[str, None] = "b2c3d4e5f6a7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "gemeinde",
        sa.Column(
            "standard_ziel_set_id",
            sa.Integer(),
            nullable=True,
            comment="ID des Standard-Leitziele-Sets dieser Gemeinde",
        ),
    )
    op.create_foreign_key(
        op.f("gemeinde_standard_ziel_set_id_fkey"),
        "gemeinde",
        "mobilitaetscheck_ziel_set",
        ["standard_ziel_set_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("gemeinde_standard_ziel_set_id_fkey"),
        "gemeinde",
        type_="foreignkey",
    )
    op.drop_column("gemeinde", "standard_ziel_set_id")
