from typing import List

from fastapi import APIRouter, Depends, status, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.klimarelevanzpruefung_eingabe import (
    crud_klimarelevanzpruefung_eingabe as crud,
)
from app.core.deps import current_active_user, get_async_session
from app.models.user import User
from app.schemas.klimarelevanzpruefung_eingabe import (
    KlimarelevanzpruefungEingabeCreate as CreateSchema,
    KlimarelevanzpruefungEingabeUpdate as UpdateSchema,
    KlimarelevanzpruefungEingabeRead as ReadSchema,
)
from app.utils.auth_util import check_user_authorization

router = APIRouter()


@router.get(
    "", response_model=List[ReadSchema], dependencies=[Depends(current_active_user)]
)
async def get_klimarelevanzpruefung_eingabe(
    db: AsyncSession = Depends(get_async_session),
):
    return await crud.get_all(db)


@router.get(
    "/magistratsvorlage/{magistratsvorlage_id}",
    response_model=List[ReadSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(current_active_user)],
)
async def get_klimarelevanzpruefung(
    magistratsvorlage_id: int,
    db: AsyncSession = Depends(get_async_session),
):
    sort_params = [("erstellt_am", "desc")]

    instances = await crud.get_by_key(
        db=db,
        key="magistratsvorlage_id",
        value=magistratsvorlage_id,
        sort_params=sort_params,
    )

    if not instances:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return instances


@router.get(
    "/{id}",
    response_model=ReadSchema,
    dependencies=[Depends(current_active_user)],
)
async def get_klimarelevanzpruefung_eingabe(
    id: int, db: AsyncSession = Depends(get_async_session)
):
    return await crud.get(db, id)


@router.get("/export/{id}", status_code=status.HTTP_201_CREATED)
async def export_klimarelevanzpruefung(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    pdf_export = await crud.export(db, id)

    filename = f"klimarelevanzpruefung_{id}.pdf"
    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return StreamingResponse(pdf_export, media_type="application/pdf", headers=headers)


@router.post(
    "",
    response_model=ReadSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_klimarelevanzpruefung_eingabe(
    obj_in: CreateSchema,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    return await crud.create(db, obj_in, user=user)


@router.patch(
    "/{id}",
    response_model=ReadSchema,
)
async def update_klimarelevanzpruefung_eingabe(
    id: int,
    updates: UpdateSchema,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    return await crud.update(db, id, updates)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_klimarelevanzpruefung_eingabe(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    return await crud.delete(db, id)
