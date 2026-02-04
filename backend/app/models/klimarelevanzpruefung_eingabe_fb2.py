from typing import Optional, List

from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class KlimarelevanzpruefungEingabeFb2(Base):
    __tablename__ = "klimarelevanzpruefung_eingabe_fb2"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="Gemeindeeinehit ID",
    )
    b1q1: Mapped[int] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=False,
        comment="Teil 1 Frage 1",
    )
    b1q2: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 1 Frage 2",
    )
    b1q3: Mapped[Optional[str]] = mapped_column(
        nullable=True,
        comment="Teil 1 Frage 3",
    )
    b1q4: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 1 Frage 4",
    )
    b1q5: Mapped[Optional[str]] = mapped_column(nullable=True, comment="Teil 1 Frage 5")
    b1q6: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 1 Frage 6",
    )
    b1q7: Mapped[Optional[str]] = mapped_column(nullable=True, comment="Teil 1 Frage 7")
    b1q8: Mapped[Optional[str]] = mapped_column(nullable=True, comment="Teil 1 Frage 8")
    b1q9: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 1 Frage 9",
    )
    b1q10: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Teil 1 Frage 10"
    )
    b1q11: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Teil 1 Frage 11"
    )
    b1q12: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 1 Frage 12",
    )
    b1q13: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Teil 1 Frage 13"
    )
    b1q14: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Teil 1 Frage 14"
    )
    b1q15: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 1 Frage 15",
    )
    b1q16: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Teil 1 Frage 16"
    )
    b1q17: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Teil 1 Frage 17"
    )
    b1q18: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 1 Frage 18",
    )
    b1q19: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Teil 1 Frage 19"
    )
    b1q20: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Teil 1 Frage 20"
    )

    b2q1: Mapped[int] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=False,
        comment="Teil 2 Frage 1",
    )
    b2q2: Mapped[Optional[str]] = mapped_column(
        nullable=True,
        comment="Teil 2 Frage 2",
    )
    b2q3: Mapped[Optional[str]] = mapped_column(
        nullable=True,
        comment="Teil 2 Frage 3",
    )
    b2q4: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 2 Frage 4",
    )
    b2q5: Mapped[Optional[str]] = mapped_column(nullable=True, comment="Teil 2 Frage 5")
