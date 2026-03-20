"""link mobilitaetscheck to ziel set

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-03-17 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision: str = "b2c3d4e5f6a7"
down_revision: Union[str, None] = "a1b2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add ziel_set_id (nullable) to mobilitaetscheck_eingabe
    op.add_column(
        "mobilitaetscheck_eingabe",
        sa.Column(
            "ziel_set_id",
            sa.Integer(),
            nullable=True,
            comment="ID des Leitziele-Sets, auf dem dieser Mobilitätscheck basiert",
        ),
    )
    op.create_foreign_key(
        op.f("mobilitaetscheck_eingabe_ziel_set_id_fkey"),
        "mobilitaetscheck_eingabe",
        "mobilitaetscheck_ziel_set",
        ["ziel_set_id"],
        ["id"],
        ondelete="SET NULL",
    )

    # 2. Data migration: assign Standard-Leitziele set per Gemeinde
    conn = op.get_bind()
    conn.execute(
        text(
            """
            UPDATE mobilitaetscheck_eingabe e
            SET ziel_set_id = (
                SELECT s.id FROM mobilitaetscheck_ziel_set s
                WHERE s.gemeinde_id = e.gemeinde_id
                AND s.name = 'Standard-Leitziele'
                ORDER BY s.id
                LIMIT 1
            )
            """
        )
    )

    # 3. Migrate mobilitaetscheck_eingabe_ziel_ober.ziel_ober_id
    #    from mobilitaetscheck_ziel_ober.id -> mobilitaetscheck_ziel_set_ober.id

    # a. Drop old FK constraint
    op.drop_constraint(
        "mobilitaetscheck_eingabe_ziel_ober_ziel_ober_id_fkey",
        "mobilitaetscheck_eingabe_ziel_ober",
        type_="foreignkey",
    )

    # b. Add temp column
    op.add_column(
        "mobilitaetscheck_eingabe_ziel_ober",
        sa.Column("ziel_set_ober_id_new", sa.Integer(), nullable=True),
    )

    # c. Populate temp column
    conn.execute(
        text(
            """
            UPDATE mobilitaetscheck_eingabe_ziel_ober ezo
            SET ziel_set_ober_id_new = (
                SELECT mzso.id
                FROM mobilitaetscheck_ziel_set_ober mzso
                JOIN mobilitaetscheck_eingabe e ON e.id = ezo.eingabe_id
                JOIN mobilitaetscheck_ziel_ober mzo ON mzo.id = ezo.ziel_ober_id
                WHERE mzso.ziel_set_id = e.ziel_set_id
                AND mzso.nr = mzo.nr
            )
            """
        )
    )

    # d. Drop old column ziel_ober_id
    op.drop_column("mobilitaetscheck_eingabe_ziel_ober", "ziel_ober_id")

    # e. Rename temp column to ziel_ober_id
    op.alter_column(
        "mobilitaetscheck_eingabe_ziel_ober",
        "ziel_set_ober_id_new",
        new_column_name="ziel_ober_id",
    )

    # f. Set NOT NULL
    op.alter_column(
        "mobilitaetscheck_eingabe_ziel_ober",
        "ziel_ober_id",
        nullable=False,
    )

    # g. Add new FK to mobilitaetscheck_ziel_set_ober
    op.create_foreign_key(
        op.f("mobilitaetscheck_eingabe_ziel_ober_ziel_ober_id_fkey"),
        "mobilitaetscheck_eingabe_ziel_ober",
        "mobilitaetscheck_ziel_set_ober",
        ["ziel_ober_id"],
        ["id"],
    )

    # 4. Migrate mobilitaetscheck_eingabe_ziel_unter.ziel_unter_id
    #    from mobilitaetscheck_ziel_unter.id -> mobilitaetscheck_ziel_set_unter.id

    # a. Drop old FK constraint
    op.drop_constraint(
        "mobilitaetscheck_eingabe_ziel_unter_ziel_unter_id_fkey",
        "mobilitaetscheck_eingabe_ziel_unter",
        type_="foreignkey",
    )

    # b. Add temp column
    op.add_column(
        "mobilitaetscheck_eingabe_ziel_unter",
        sa.Column("ziel_set_unter_id_new", sa.Integer(), nullable=True),
    )

    # c. Populate temp column (ezo.ziel_ober_id already points to ziel_set_ober)
    conn.execute(
        text(
            """
            UPDATE mobilitaetscheck_eingabe_ziel_unter ezu
            SET ziel_set_unter_id_new = (
                SELECT mzsu.id
                FROM mobilitaetscheck_ziel_set_unter mzsu
                JOIN mobilitaetscheck_eingabe_ziel_ober ezo ON ezo.id = ezu.eingabe_ziel_ober_id
                JOIN mobilitaetscheck_ziel_unter mzu ON mzu.id = ezu.ziel_unter_id
                WHERE mzsu.ziel_set_ober_id = ezo.ziel_ober_id
                AND mzsu.nr = mzu.nr
            )
            """
        )
    )

    # d. Drop old column ziel_unter_id
    op.drop_column("mobilitaetscheck_eingabe_ziel_unter", "ziel_unter_id")

    # e. Rename temp column to ziel_unter_id
    op.alter_column(
        "mobilitaetscheck_eingabe_ziel_unter",
        "ziel_set_unter_id_new",
        new_column_name="ziel_unter_id",
    )

    # f. Set NOT NULL
    op.alter_column(
        "mobilitaetscheck_eingabe_ziel_unter",
        "ziel_unter_id",
        nullable=False,
    )

    # g. Add new FK to mobilitaetscheck_ziel_set_unter with CASCADE
    op.create_foreign_key(
        op.f("mobilitaetscheck_eingabe_ziel_unter_ziel_unter_id_fkey"),
        "mobilitaetscheck_eingabe_ziel_unter",
        "mobilitaetscheck_ziel_set_unter",
        ["ziel_unter_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    conn = op.get_bind()

    # --- Reverse ziel_unter migration ---

    # Drop new FK
    op.drop_constraint(
        op.f("mobilitaetscheck_eingabe_ziel_unter_ziel_unter_id_fkey"),
        "mobilitaetscheck_eingabe_ziel_unter",
        type_="foreignkey",
    )

    # Add temp column
    op.add_column(
        "mobilitaetscheck_eingabe_ziel_unter",
        sa.Column("ziel_ober_id_old", sa.Integer(), nullable=True),
    )

    # Reverse data: map ziel_set_unter.id back to ziel_unter.id via nr matching
    conn.execute(
        text(
            """
            UPDATE mobilitaetscheck_eingabe_ziel_unter ezu
            SET ziel_ober_id_old = (
                SELECT mzu.id
                FROM mobilitaetscheck_ziel_unter mzu
                JOIN mobilitaetscheck_ziel_set_unter mzsu ON mzsu.id = ezu.ziel_unter_id
                JOIN mobilitaetscheck_eingabe_ziel_ober ezo ON ezo.id = ezu.eingabe_ziel_ober_id
                JOIN mobilitaetscheck_eingabe e ON e.id = ezo.eingabe_id
                JOIN mobilitaetscheck_ziel_ober mzo ON mzo.gemeinde_id = e.gemeinde_id AND mzo.nr = mzsu.nr
                WHERE mzu.ziel_ober_id = mzo.id
                AND mzu.nr = mzsu.nr
                LIMIT 1
            )
            """
        )
    )

    op.drop_column("mobilitaetscheck_eingabe_ziel_unter", "ziel_unter_id")
    op.alter_column(
        "mobilitaetscheck_eingabe_ziel_unter",
        "ziel_ober_id_old",
        new_column_name="ziel_unter_id",
    )
    op.alter_column(
        "mobilitaetscheck_eingabe_ziel_unter",
        "ziel_unter_id",
        nullable=False,
    )
    op.create_foreign_key(
        "mobilitaetscheck_eingabe_ziel_unter_ziel_unter_id_fkey",
        "mobilitaetscheck_eingabe_ziel_unter",
        "mobilitaetscheck_ziel_unter",
        ["ziel_unter_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # --- Reverse ziel_ober migration ---

    # Drop new FK
    op.drop_constraint(
        op.f("mobilitaetscheck_eingabe_ziel_ober_ziel_ober_id_fkey"),
        "mobilitaetscheck_eingabe_ziel_ober",
        type_="foreignkey",
    )

    # Add temp column
    op.add_column(
        "mobilitaetscheck_eingabe_ziel_ober",
        sa.Column("ziel_ober_id_old", sa.Integer(), nullable=True),
    )

    # Reverse data: map ziel_set_ober.id back to ziel_ober.id via nr matching
    conn.execute(
        text(
            """
            UPDATE mobilitaetscheck_eingabe_ziel_ober ezo
            SET ziel_ober_id_old = (
                SELECT mzo.id
                FROM mobilitaetscheck_ziel_ober mzo
                JOIN mobilitaetscheck_ziel_set_ober mzso ON mzso.id = ezo.ziel_ober_id
                JOIN mobilitaetscheck_eingabe e ON e.id = ezo.eingabe_id
                WHERE mzo.gemeinde_id = e.gemeinde_id
                AND mzo.nr = mzso.nr
                LIMIT 1
            )
            """
        )
    )

    op.drop_column("mobilitaetscheck_eingabe_ziel_ober", "ziel_ober_id")
    op.alter_column(
        "mobilitaetscheck_eingabe_ziel_ober",
        "ziel_ober_id_old",
        new_column_name="ziel_ober_id",
    )
    op.alter_column(
        "mobilitaetscheck_eingabe_ziel_ober",
        "ziel_ober_id",
        nullable=False,
    )
    op.create_foreign_key(
        "mobilitaetscheck_eingabe_ziel_ober_ziel_ober_id_fkey",
        "mobilitaetscheck_eingabe_ziel_ober",
        "mobilitaetscheck_ziel_ober",
        ["ziel_ober_id"],
        ["id"],
    )

    # --- Reverse eingabe ziel_set_id migration ---

    op.drop_constraint(
        op.f("mobilitaetscheck_eingabe_ziel_set_id_fkey"),
        "mobilitaetscheck_eingabe",
        type_="foreignkey",
    )
    op.drop_column("mobilitaetscheck_eingabe", "ziel_set_id")
