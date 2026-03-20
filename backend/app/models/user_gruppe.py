from typing import List, Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base


class UserGruppe(Base):
    __tablename__ = "user_gruppe"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True, comment="Gruppe ID")
    name: Mapped[str] = mapped_column(nullable=False, comment="Name der Gruppe")
    gemeinde_id: Mapped[int] = mapped_column(
        ForeignKey("gemeinde.id", ondelete="CASCADE"), nullable=False, comment="Gemeinde ID"
    )
    gemeinde: Mapped["Gemeinde"] = relationship(lazy="selectin")
    rolle_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("user_rolle.id", ondelete="SET NULL"), nullable=True, comment="Rolle, für die diese Gruppe gilt"
    )
    rolle: Mapped[Optional["UserRolle"]] = relationship(lazy="selectin")
    users: Mapped[Optional[List["User"]]] = relationship(back_populates="gruppe", lazy="selectin")


from app.models.gemeinde import Gemeinde
from app.models.user import User
from app.models.user_rolle import UserRolle
