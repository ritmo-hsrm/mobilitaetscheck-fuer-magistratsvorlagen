"""add a5q5 to klimarelevanzpruefung_eingabe_fb1

Revision ID: f7a8b9c0d1e2
Revises: a2b3c4d5e6f7
Create Date: 2026-03-31 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f7a8b9c0d1e2"
down_revision: Union[str, None] = "a2b3c4d5e6f7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "klimarelevanzpruefung_eingabe_fb1",
        sa.Column("a5q5", sa.String(), nullable=True, comment="Teil 5 Frage 5"),
    )
    op.execute(
        "INSERT INTO klimarelevanzpruefung_vorhaben (id, name) "
        "SELECT COALESCE(MAX(id), 0) + 1, 'Sonstiges' FROM klimarelevanzpruefung_vorhaben"
    )


def downgrade() -> None:
    op.execute("DELETE FROM klimarelevanzpruefung_vorhaben WHERE name = 'Sonstiges'")
    op.drop_column("klimarelevanzpruefung_eingabe_fb1", "a5q5")
