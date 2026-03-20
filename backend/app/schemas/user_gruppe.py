from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class UserGruppeCreate(BaseModel):
    name: str = Field(..., description="Name der Gruppe")
    gemeinde_id: Optional[int] = Field(None, description="ID der Gemeinde")
    rolle_id: Optional[int] = Field(None, description="Rolle, für die diese Gruppe gilt")


class UserGruppeUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Name der Gruppe")


class UserGruppeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    gemeinde_id: int
    rolle_id: Optional[int] = None


class GruppeUserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    vorname: str
    nachname: str
    email: str
    gruppe_id: Optional[int] = None
    rolle_name: Optional[str] = None


class GruppeUserUpdate(BaseModel):
    gruppe_id: Optional[int] = None
