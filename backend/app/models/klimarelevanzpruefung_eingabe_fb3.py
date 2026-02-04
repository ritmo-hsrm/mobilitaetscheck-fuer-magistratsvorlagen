from typing import Optional, List

from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class KlimarelevanzpruefungEingabeFb3(Base):
    __tablename__ = "klimarelevanzpruefung_eingabe_fb3"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="Gemeindeeinehit ID",
    )
    c1q1: Mapped[int] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=False,
        comment="Teil 1 Frage 1",
    )
    c1q2: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 1 Frage 2",
    )
    c1q3: Mapped[Optional[str]] = mapped_column(
        nullable=True,
        comment="Teil 1 Frage 3",
    )
    c1q4: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 1 Frage 4",
    )
    c1q5: Mapped[Optional[str]] = mapped_column(nullable=True, comment="Teil 1 Frage 5")
    c1q6: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 1 Frage 6",
    )
    c1q7: Mapped[Optional[str]] = mapped_column(nullable=True, comment="Teil 1 Frage 7")
    c1q8: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 1 Frage 8",
    )
    c1q9: Mapped[Optional[str]] = mapped_column(
        nullable=True,
        comment="Teil 1 Frage 9",
    )

    c2q1: Mapped[int] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=False,
        comment="Teil 2 Frage 1",
    )
    c2q2: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 2 Frage 2",
    )
    c2q3: Mapped[Optional[str]] = mapped_column(
        nullable=True,
        comment="Teil 2 Frage 3",
    )
    c2q4: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 2 Frage 4",
    )
    c2q5: Mapped[Optional[str]] = mapped_column(nullable=True, comment="Teil 2 Frage 5")
    c2q6: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 2 Frage 6",
    )
    c2q7: Mapped[Optional[str]] = mapped_column(nullable=True, comment="Teil 2 Frage 7")
    c2q8: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 2 Frage 8",
    )
    c2q9: Mapped[Optional[str]] = mapped_column(nullable=True, comment="Teil 2 Frage 9")
