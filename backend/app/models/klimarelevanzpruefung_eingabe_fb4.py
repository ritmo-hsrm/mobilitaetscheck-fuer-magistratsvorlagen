from typing import Optional, List

from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class KlimarelevanzpruefungEingabeFb4(Base):
    __tablename__ = "klimarelevanzpruefung_eingabe_fb4"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="Gemeindeeinehit ID",
    )
    d1q1: Mapped[str] = mapped_column(
        nullable=False,
        comment="Teil 1 Frage 1",
    )

    d2q1: Mapped[str] = mapped_column(
        nullable=False,
        comment="Teil 2 Frage 1",
    )
