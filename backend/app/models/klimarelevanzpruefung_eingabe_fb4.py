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
    fertig: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
        server_default="false",
        comment="Fragebogen vollständig ausgefüllt",
    )

    d1q1: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 1 Frage 1",
    )
    d1q2: Mapped[Optional[str]] = mapped_column(
        nullable=True,
        comment="Teil 1 Frage 2",
    )
    d2q1: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 2 Frage 1",
    )
    d2q2: Mapped[Optional[str]] = mapped_column(
        nullable=True,
        comment="Teil 2 Frage 2",
    )
