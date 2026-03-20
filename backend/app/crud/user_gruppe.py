from app.crud.base import CRUDBase
from app.models.user_gruppe import UserGruppe as Model
from app.schemas.user_gruppe import UserGruppeCreate as CreateSchema, UserGruppeUpdate as UpdateSchema


class CRUDUserGruppe(CRUDBase[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)


crud_user_gruppe = CRUDUserGruppe()
