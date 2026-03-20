from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class GemeindeBase(BaseModel):
    """
    Base schema for a Gemeinde, containing the primary name attribute.
    """

    name: str = Field(..., description="The name of the Gemeinde.")
    verwaltung_email_domain: Optional[str] = Field(None, description="Erlaubte E-Mail-Domain für Verwaltung-Benutzer (z.B. muenchen.de).")


class GemeindeCreate(GemeindeBase):
    """
    Schema for creating a new Gemeinde. Inherits fields from GemeindeBase.
    """

    pass


class GemeindeUpdate(BaseModel):
    """
    Schema for updating an existing Gemeinde. Allows partial updates.
    """

    name: Optional[str] = Field(None, description="The updated name of the Gemeinde.")
    verwaltung_email_domain: Optional[str] = Field(None, description="Erlaubte E-Mail-Domain für Verwaltung-Benutzer (z.B. muenchen.de).")


class GemeindeRead(GemeindeBase):
    """
    Read schema for a Gemeinde, including the unique identifier.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier for the Gemeinde.")
    standard_ziel_set_id: Optional[int] = Field(None, description="ID des Standard-Leitziele-Sets.")
    verwaltung_email_domain: Optional[str] = Field(None, description="Erlaubte E-Mail-Domain für Verwaltung-Benutzer.")
