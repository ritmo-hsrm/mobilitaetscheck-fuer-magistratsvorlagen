"""cascade delete eingabe_ziel_ober when ziel_set_ober is deleted

Revision ID: e5f6a7b8c9d0
Revises: d4e5f6a7b8c9
Create Date: 2026-03-18 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "e5f6a7b8c9d0"
down_revision: Union[str, None] = "d4e5f6a7b8c9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        op.f("mobilitaetscheck_eingabe_ziel_ober_ziel_ober_id_fkey"),
        "mobilitaetscheck_eingabe_ziel_ober",
        type_="foreignkey",
    )
    op.create_foreign_key(
        op.f("mobilitaetscheck_eingabe_ziel_ober_ziel_ober_id_fkey"),
        "mobilitaetscheck_eingabe_ziel_ober",
        "mobilitaetscheck_ziel_set_ober",
        ["ziel_ober_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("mobilitaetscheck_eingabe_ziel_ober_ziel_ober_id_fkey"),
        "mobilitaetscheck_eingabe_ziel_ober",
        type_="foreignkey",
    )
    op.create_foreign_key(
        op.f("mobilitaetscheck_eingabe_ziel_ober_ziel_ober_id_fkey"),
        "mobilitaetscheck_eingabe_ziel_ober",
        "mobilitaetscheck_ziel_set_ober",
        ["ziel_ober_id"],
        ["id"],
    )
