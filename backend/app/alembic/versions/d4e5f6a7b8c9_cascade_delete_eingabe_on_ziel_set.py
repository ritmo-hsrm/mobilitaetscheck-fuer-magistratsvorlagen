"""cascade delete eingabe when ziel_set is deleted

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2026-03-18 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d4e5f6a7b8c9"
down_revision: Union[str, None] = "c3d4e5f6a7b8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        op.f("mobilitaetscheck_eingabe_ziel_set_id_fkey"),
        "mobilitaetscheck_eingabe",
        type_="foreignkey",
    )
    op.create_foreign_key(
        op.f("mobilitaetscheck_eingabe_ziel_set_id_fkey"),
        "mobilitaetscheck_eingabe",
        "mobilitaetscheck_ziel_set",
        ["ziel_set_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("mobilitaetscheck_eingabe_ziel_set_id_fkey"),
        "mobilitaetscheck_eingabe",
        type_="foreignkey",
    )
    op.create_foreign_key(
        op.f("mobilitaetscheck_eingabe_ziel_set_id_fkey"),
        "mobilitaetscheck_eingabe",
        "mobilitaetscheck_ziel_set",
        ["ziel_set_id"],
        ["id"],
        ondelete="SET NULL",
    )
