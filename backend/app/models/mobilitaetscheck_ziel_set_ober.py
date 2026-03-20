from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class MobilitaetscheckZielSetOber(Base):
    __tablename__ = "mobilitaetscheck_ziel_set_ober"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="ID des Oberziels im Set",
    )
    nr: Mapped[int] = mapped_column(
        nullable=False, comment="Nummerierung des Oberziels im Set"
    )
    name: Mapped[str] = mapped_column(
        nullable=False, comment="Name des Oberziels im Set"
    )
    ziel_set_id: Mapped[int] = mapped_column(
        ForeignKey("mobilitaetscheck_ziel_set.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID des Leitziele-Sets",
    )
    ziel_set: Mapped["MobilitaetscheckZielSet"] = relationship(
        back_populates="ziele_ober", lazy="selectin"
    )
    ziele_unter: Mapped[List["MobilitaetscheckZielSetUnter"]] = relationship(
        back_populates="ziel_set_ober",
        cascade="all, delete",
        lazy="selectin",
    )


# Late imports
from app.models.mobilitaetscheck_ziel_set import MobilitaetscheckZielSet
from app.models.mobilitaetscheck_ziel_set_unter import MobilitaetscheckZielSetUnter
