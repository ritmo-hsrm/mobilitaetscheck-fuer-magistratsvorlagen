"""add verwaltung_email_domain to gemeinde

Revision ID: c4d5e6f7a8b9
Revises: b3c4d5e6f7a8
Create Date: 2026-03-19 00:00:00.000000
"""
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op

revision: str = "c4d5e6f7a8b9"
down_revision: Union[str, None] = "b3c4d5e6f7a8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "gemeinde",
        sa.Column(
            "verwaltung_email_domain",
            sa.String(),
            nullable=True,
            comment="Erlaubte E-Mail-Domain für Verwaltung-Benutzer (z.B. muenchen.de)",
        ),
    )


def downgrade() -> None:
    op.drop_column("gemeinde", "verwaltung_email_domain")
