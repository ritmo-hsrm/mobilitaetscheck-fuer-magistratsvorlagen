"""update fb4: add yes/no questions d1q1 and d2q1, add justification fields d1q2 and d2q2

Revision ID: a2b3c4d5e6f7
Revises: d5e6f7a8b9c0
Create Date: 2026-03-31 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a2b3c4d5e6f7"
down_revision: Union[str, None] = "d5e6f7a8b9c0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add new justification columns (nullable)
    op.add_column(
        "klimarelevanzpruefung_eingabe_fb4",
        sa.Column("d1q2", sa.String(), nullable=True, comment="Teil 1 Frage 2"),
    )
    op.add_column(
        "klimarelevanzpruefung_eingabe_fb4",
        sa.Column("d2q2", sa.String(), nullable=True, comment="Teil 2 Frage 2"),
    )

    # Copy old text data from d1q1 -> d1q2 and d2q1 -> d2q2 before type change
    op.execute(
        "UPDATE klimarelevanzpruefung_eingabe_fb4 SET d1q2 = d1q1, d2q2 = d2q1"
    )

    # Drop old string columns
    op.drop_column("klimarelevanzpruefung_eingabe_fb4", "d1q1")
    op.drop_column("klimarelevanzpruefung_eingabe_fb4", "d2q1")

    # Add new integer columns with FK to bool_erweitert (nullable)
    op.add_column(
        "klimarelevanzpruefung_eingabe_fb4",
        sa.Column(
            "d1q1",
            sa.Integer(),
            sa.ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
            nullable=True,
            comment="Teil 1 Frage 1",
        ),
    )
    op.add_column(
        "klimarelevanzpruefung_eingabe_fb4",
        sa.Column(
            "d2q1",
            sa.Integer(),
            sa.ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
            nullable=True,
            comment="Teil 2 Frage 1",
        ),
    )


def downgrade() -> None:
    # Drop FK integer columns
    op.drop_column("klimarelevanzpruefung_eingabe_fb4", "d1q1")
    op.drop_column("klimarelevanzpruefung_eingabe_fb4", "d2q1")

    # Re-add original string columns (data from d1q2/d2q2 is restored)
    op.add_column(
        "klimarelevanzpruefung_eingabe_fb4",
        sa.Column("d1q1", sa.String(), nullable=True, comment="Teil 1 Frage 1"),
    )
    op.add_column(
        "klimarelevanzpruefung_eingabe_fb4",
        sa.Column("d2q1", sa.String(), nullable=True, comment="Teil 2 Frage 1"),
    )

    # Restore text data
    op.execute(
        "UPDATE klimarelevanzpruefung_eingabe_fb4 SET d1q1 = d1q2, d2q1 = d2q2"
    )

    # Drop justification columns
    op.drop_column("klimarelevanzpruefung_eingabe_fb4", "d1q2")
    op.drop_column("klimarelevanzpruefung_eingabe_fb4", "d2q2")
