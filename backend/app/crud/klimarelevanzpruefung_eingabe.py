from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base_eingabe import CRUDEingabe
from app.models.klimarelevanzpruefung_eingabe import (
    KlimarelevanzpruefungEingabe as Model,
)
from app.services.pdf.klimarelevanzpruefung_pdf import KlimarelevanzpruefungPDF

from app.schemas.klimarelevanzpruefung_eingabe import (
    KlimarelevanzpruefungEingabeCreate as CreateSchema,
    KlimarelevanzpruefungEingabeUpdate as UpdateSchema,
)


class CRUDKlimarelevanzpruefungEingabe(CRUDEingabe[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)

    async def export(self, db: AsyncSession, id: int):
        return await super().export(db=db, id=id, PDF=KlimarelevanzpruefungPDF)


crud_klimarelevanzpruefung_eingabe = CRUDKlimarelevanzpruefungEingabe()
