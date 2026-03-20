from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict, computed_field


# --- ZielSetUnter schemas ---

class MobilitaetscheckZielSetUnterBase(BaseModel):
    nr: int = Field(..., description="Nummerierung des Unterziels im Set")
    name: str = Field(..., description="Name des Unterziels im Set")


class MobilitaetscheckZielSetUnterCreate(MobilitaetscheckZielSetUnterBase):
    pass


class MobilitaetscheckZielSetUnterRead(MobilitaetscheckZielSetUnterBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# --- ZielSetOber schemas ---

class MobilitaetscheckZielSetOberBase(BaseModel):
    nr: int = Field(..., description="Nummerierung des Oberziels im Set")
    name: str = Field(..., description="Name des Oberziels im Set")


class MobilitaetscheckZielSetOberCreate(MobilitaetscheckZielSetOberBase):
    ziele_unter: List[MobilitaetscheckZielSetUnterCreate] = Field(default_factory=list)


class MobilitaetscheckZielSetOberRead(MobilitaetscheckZielSetOberBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    ziele_unter: List[MobilitaetscheckZielSetUnterRead] = Field(default_factory=list)


# --- ZielSet schemas ---

class MobilitaetscheckZielSetBase(BaseModel):
    name: str = Field(..., description="Name des Leitziele-Sets")
    beschreibung: Optional[str] = Field(None, description="Beschreibung des Sets")
    ist_oeffentlich: bool = Field(False, description="Ob das Set öffentlich sichtbar ist")


class MobilitaetscheckZielSetCreate(MobilitaetscheckZielSetBase):
    ziele_ober: List[MobilitaetscheckZielSetOberCreate] = Field(default_factory=list)


class MobilitaetscheckZielSetUpdate(BaseModel):
    name: Optional[str] = Field(None)
    beschreibung: Optional[str] = Field(None)
    ist_oeffentlich: Optional[bool] = Field(None)


class MobilitaetscheckZielSetRead(MobilitaetscheckZielSetBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    gemeinde_id: int
    gemeinde: "GemeindeRead"
    ziele_ober: List[MobilitaetscheckZielSetOberRead] = Field(default_factory=list)
    autor: Optional["UserRead"] = None
    letzter_bearbeiter: Optional["UserRead"] = None


class MobilitaetscheckZielSetListRead(MobilitaetscheckZielSetBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    gemeinde_id: int
    gemeinde: "GemeindeRead"
    autor: Optional["UserRead"] = None
    ist_standard: bool = False
    ziele_ober: List[MobilitaetscheckZielSetOberRead] = Field(default_factory=list, exclude=True)

    @computed_field
    @property
    def hat_ziele(self) -> bool:
        return len(self.ziele_ober) > 0


class MobilitaetscheckZielSetKopierenRequest(BaseModel):
    modus: str = Field("anhaengen", description="'ersetzen' oder 'anhaengen'")


# Late imports
from app.schemas.gemeinde import GemeindeRead
from app.schemas.user import UserRead
