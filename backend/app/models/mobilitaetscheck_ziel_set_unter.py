from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class MobilitaetscheckZielSetUnter(Base):
    __tablename__ = "mobilitaetscheck_ziel_set_unter"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="ID des Unterziels im Set",
    )
    nr: Mapped[int] = mapped_column(
        nullable=False, comment="Nummerierung des Unterziels im Set"
    )
    name: Mapped[str] = mapped_column(
        nullable=False, comment="Name des Unterziels im Set"
    )
    ziel_set_ober_id: Mapped[int] = mapped_column(
        ForeignKey("mobilitaetscheck_ziel_set_ober.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID des Oberziels im Set",
    )
    ziel_set_ober: Mapped["MobilitaetscheckZielSetOber"] = relationship(
        back_populates="ziele_unter", lazy="selectin"
    )


# Late imports
from app.models.mobilitaetscheck_ziel_set_ober import MobilitaetscheckZielSetOber
