from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class KlimarelevanzpruefungEingabeFb4Base(BaseModel):

    fertig: bool = False
    d1q1: Optional[int] = None
    d1q2: Optional[str] = None
    d2q1: Optional[int] = None
    d2q2: Optional[str] = None


class KlimarelevanzpruefungEingabeFb4Create(KlimarelevanzpruefungEingabeFb4Base):
    pass


class KlimarelevanzpruefungEingabeFb4Update(BaseModel):
    fertig: Optional[bool] = None
    d1q1: Optional[int] = None
    d1q2: Optional[str] = None
    d2q1: Optional[int] = None
    d2q2: Optional[str] = None


class KlimarelevanzpruefungEingabeFb4Read(KlimarelevanzpruefungEingabeFb4Base):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Kennung für das Item.")
