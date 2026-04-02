"""add fertig to klimarelevanzpruefung

Revision ID: f37510ecaac5
Revises: f7a8b9c0d1e2
Create Date: 2026-03-31 19:45:13.873886

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "f37510ecaac5"
down_revision: Union[str, None] = "f7a8b9c0d1e2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add fertig column to all fb tables
    for table in [
        "klimarelevanzpruefung_eingabe_fb1",
        "klimarelevanzpruefung_eingabe_fb2",
        "klimarelevanzpruefung_eingabe_fb3",
        "klimarelevanzpruefung_eingabe_fb4",
    ]:
        op.add_column(
            table,
            sa.Column(
                "fertig",
                sa.Boolean(),
                nullable=False,
                server_default="false",
                comment="Fragebogen vollständig ausgefüllt",
            ),
        )

    # Make previously required fields nullable in fb1
    for col in ["a1q1", "a2q1", "a3q1", "a4q1", "a5q1", "a6q1", "a7q1", "a8q1"]:
        op.alter_column(
            "klimarelevanzpruefung_eingabe_fb1",
            col,
            existing_type=sa.Integer(),
            nullable=True,
        )

    # Make previously required fields nullable in fb2
    for col in ["b1q1", "b2q1"]:
        op.alter_column(
            "klimarelevanzpruefung_eingabe_fb2",
            col,
            existing_type=sa.Integer(),
            nullable=True,
        )

    # Make previously required fields nullable in fb3
    for col in ["c1q1", "c2q1"]:
        op.alter_column(
            "klimarelevanzpruefung_eingabe_fb3",
            col,
            existing_type=sa.Integer(),
            nullable=True,
        )


def downgrade() -> None:
    # Reverse nullable changes for fb3
    for col in ["c1q1", "c2q1"]:
        op.alter_column(
            "klimarelevanzpruefung_eingabe_fb3",
            col,
            existing_type=sa.Integer(),
            nullable=False,
        )

    # Reverse nullable changes for fb2
    for col in ["b1q1", "b2q1"]:
        op.alter_column(
            "klimarelevanzpruefung_eingabe_fb2",
            col,
            existing_type=sa.Integer(),
            nullable=False,
        )

    # Reverse nullable changes for fb1
    for col in ["a1q1", "a2q1", "a3q1", "a4q1", "a5q1", "a6q1", "a7q1", "a8q1"]:
        op.alter_column(
            "klimarelevanzpruefung_eingabe_fb1",
            col,
            existing_type=sa.Integer(),
            nullable=False,
        )

    # Drop fertig columns
    for table in [
        "klimarelevanzpruefung_eingabe_fb4",
        "klimarelevanzpruefung_eingabe_fb3",
        "klimarelevanzpruefung_eingabe_fb2",
        "klimarelevanzpruefung_eingabe_fb1",
    ]:
        op.drop_column(table, "fertig")
