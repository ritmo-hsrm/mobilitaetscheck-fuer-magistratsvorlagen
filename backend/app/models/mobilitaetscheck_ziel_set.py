from typing import List, Optional

from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class MobilitaetscheckZielSet(Base):
    __tablename__ = "mobilitaetscheck_ziel_set"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="ID des Leitziele-Sets",
    )
    name: Mapped[str] = mapped_column(
        nullable=False, comment="Name des Leitziele-Sets"
    )
    beschreibung: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="Beschreibung des Leitziele-Sets"
    )
    ist_oeffentlich: Mapped[bool] = mapped_column(
        nullable=False, default=False, comment="Ob das Set für andere Kommunen sichtbar ist"
    )
    gemeinde_id: Mapped[int] = mapped_column(
        ForeignKey("gemeinde.id", ondelete="CASCADE"),
        nullable=False,
        comment="Gemeinde ID der erstellenden Kommune",
    )
    gemeinde: Mapped["Gemeinde"] = relationship(foreign_keys=[gemeinde_id], lazy="selectin")
    erstellt_von: Mapped[Optional[GUID]] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True,
        comment="User ID des Erstellers",
    )
    autor: Mapped[Optional["User"]] = relationship(
        foreign_keys=[erstellt_von], lazy="selectin"
    )
    zuletzt_bearbeitet_von: Mapped[Optional[GUID]] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True,
        comment="User ID des zuletzt bearbeitenden Benutzers",
    )
    letzter_bearbeiter: Mapped[Optional["User"]] = relationship(
        foreign_keys=[zuletzt_bearbeitet_von], lazy="selectin"
    )
    ziele_ober: Mapped[List["MobilitaetscheckZielSetOber"]] = relationship(
        back_populates="ziel_set",
        cascade="all, delete",
        lazy="selectin",
    )


# Late imports
from app.models.gemeinde import Gemeinde
from app.models.user import User
from app.models.mobilitaetscheck_ziel_set_ober import MobilitaetscheckZielSetOber
