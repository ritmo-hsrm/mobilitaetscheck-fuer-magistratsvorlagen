"""add leitziele sets

Revision ID: a1b2c3d4e5f6
Revises: 9fb16fcb80af
Create Date: 2026-03-17 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "9fb16fcb80af"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### Create mobilitaetscheck_ziel_set ###
    op.create_table(
        "mobilitaetscheck_ziel_set",
        sa.Column("id", sa.Integer(), nullable=False, comment="ID des Leitziele-Sets"),
        sa.Column("name", sa.String(), nullable=False, comment="Name des Leitziele-Sets"),
        sa.Column("beschreibung", sa.Text(), nullable=True, comment="Beschreibung des Leitziele-Sets"),
        sa.Column(
            "ist_oeffentlich",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
            comment="Ob das Set für andere Kommunen sichtbar ist",
        ),
        sa.Column(
            "gemeinde_id",
            sa.Integer(),
            nullable=False,
            comment="Gemeinde ID der erstellenden Kommune",
        ),
        sa.Column(
            "erstellt_von",
            sa.Uuid(),
            nullable=True,
            comment="User ID des Erstellers",
        ),
        sa.Column(
            "zuletzt_bearbeitet_von",
            sa.Uuid(),
            nullable=True,
            comment="User ID des zuletzt bearbeitenden Benutzers",
        ),
        sa.ForeignKeyConstraint(["gemeinde_id"], ["gemeinde.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["erstellt_von"], ["user.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["zuletzt_bearbeitet_von"], ["user.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.create_index(
        op.f("ix_mobilitaetscheck_ziel_set_id"),
        "mobilitaetscheck_ziel_set",
        ["id"],
        unique=False,
    )

    # ### Create mobilitaetscheck_ziel_set_ober ###
    op.create_table(
        "mobilitaetscheck_ziel_set_ober",
        sa.Column("id", sa.Integer(), nullable=False, comment="ID des Oberziels im Set"),
        sa.Column("nr", sa.Integer(), nullable=False, comment="Nummerierung des Oberziels im Set"),
        sa.Column("name", sa.String(), nullable=False, comment="Name des Oberziels im Set"),
        sa.Column(
            "ziel_set_id",
            sa.Integer(),
            nullable=False,
            comment="ID des Leitziele-Sets",
        ),
        sa.ForeignKeyConstraint(
            ["ziel_set_id"], ["mobilitaetscheck_ziel_set.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.create_index(
        op.f("ix_mobilitaetscheck_ziel_set_ober_id"),
        "mobilitaetscheck_ziel_set_ober",
        ["id"],
        unique=False,
    )

    # ### Create mobilitaetscheck_ziel_set_unter ###
    op.create_table(
        "mobilitaetscheck_ziel_set_unter",
        sa.Column("id", sa.Integer(), nullable=False, comment="ID des Unterziels im Set"),
        sa.Column("nr", sa.Integer(), nullable=False, comment="Nummerierung des Unterziels im Set"),
        sa.Column("name", sa.String(), nullable=False, comment="Name des Unterziels im Set"),
        sa.Column(
            "ziel_set_ober_id",
            sa.Integer(),
            nullable=False,
            comment="ID des Oberziels im Set",
        ),
        sa.ForeignKeyConstraint(
            ["ziel_set_ober_id"],
            ["mobilitaetscheck_ziel_set_ober.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.create_index(
        op.f("ix_mobilitaetscheck_ziel_set_unter_id"),
        "mobilitaetscheck_ziel_set_unter",
        ["id"],
        unique=False,
    )

    # ### Migrate existing Leitziele into initial sets per Gemeinde ###
    # For each Gemeinde that has existing Oberziele, create one ZielSet named
    # "Standard-Leitziele" as a snapshot of the current state.
    conn = op.get_bind()

    # Fetch all distinct Gemeinden that have Oberziele
    gemeinden = conn.execute(
        text(
            "SELECT DISTINCT gemeinde_id FROM mobilitaetscheck_ziel_ober ORDER BY gemeinde_id"
        )
    ).fetchall()

    for (gemeinde_id,) in gemeinden:
        # Insert the ZielSet for this Gemeinde
        result = conn.execute(
            text(
                "INSERT INTO mobilitaetscheck_ziel_set "
                "(name, beschreibung, ist_oeffentlich, gemeinde_id, erstellt_von, zuletzt_bearbeitet_von) "
                "VALUES (:name, :beschreibung, :ist_oeffentlich, :gemeinde_id, NULL, NULL) "
                "RETURNING id"
            ),
            {
                "name": "Standard-Leitziele",
                "beschreibung": "Automatisch migrierte Leitziele",
                "ist_oeffentlich": False,
                "gemeinde_id": gemeinde_id,
            },
        )
        ziel_set_id = result.fetchone()[0]

        # Fetch Oberziele for this Gemeinde, ordered by nr
        oberziele = conn.execute(
            text(
                "SELECT id, nr, name FROM mobilitaetscheck_ziel_ober "
                "WHERE gemeinde_id = :gemeinde_id ORDER BY nr"
            ),
            {"gemeinde_id": gemeinde_id},
        ).fetchall()

        for ober_id, ober_nr, ober_name in oberziele:
            # Insert the ZielSetOber
            result_ober = conn.execute(
                text(
                    "INSERT INTO mobilitaetscheck_ziel_set_ober (nr, name, ziel_set_id) "
                    "VALUES (:nr, :name, :ziel_set_id) RETURNING id"
                ),
                {"nr": ober_nr, "name": ober_name, "ziel_set_id": ziel_set_id},
            )
            ziel_set_ober_id = result_ober.fetchone()[0]

            # Fetch Unterziele for this Oberziel, ordered by nr
            unterziele = conn.execute(
                text(
                    "SELECT nr, name FROM mobilitaetscheck_ziel_unter "
                    "WHERE ziel_ober_id = :ziel_ober_id ORDER BY nr"
                ),
                {"ziel_ober_id": ober_id},
            ).fetchall()

            for unter_nr, unter_name in unterziele:
                conn.execute(
                    text(
                        "INSERT INTO mobilitaetscheck_ziel_set_unter (nr, name, ziel_set_ober_id) "
                        "VALUES (:nr, :name, :ziel_set_ober_id)"
                    ),
                    {"nr": unter_nr, "name": unter_name, "ziel_set_ober_id": ziel_set_ober_id},
                )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_mobilitaetscheck_ziel_set_unter_id"),
        table_name="mobilitaetscheck_ziel_set_unter",
    )
    op.drop_table("mobilitaetscheck_ziel_set_unter")
    op.drop_index(
        op.f("ix_mobilitaetscheck_ziel_set_ober_id"),
        table_name="mobilitaetscheck_ziel_set_ober",
    )
    op.drop_table("mobilitaetscheck_ziel_set_ober")
    op.drop_index(
        op.f("ix_mobilitaetscheck_ziel_set_id"),
        table_name="mobilitaetscheck_ziel_set",
    )
    op.drop_table("mobilitaetscheck_ziel_set")
