from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from app.core.deps import current_platform_admin, get_async_session
from app.crud.exceptions import NotFoundError
from app.crud.gemeinde import crud_gemeinde
from app.models.user import User
from app.models.gemeinde import Gemeinde
from app.schemas.gemeinde import GemeindeCreate, GemeindeRead, GemeindeUpdate
from app.schemas.user import UserRead

router = APIRouter()


@router.get("/gemeinde", response_model=List[GemeindeRead])
async def get_all_gemeinden(
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    try:
        return await crud_gemeinde.get_all(db=db, sort_params=[("name", "asc")])
    except NotFoundError:
        return []


@router.post("/gemeinde", response_model=GemeindeRead)
async def create_gemeinde(
    obj_in: GemeindeCreate,
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    return await crud_gemeinde.create(db=db, obj_in=obj_in)


@router.patch("/gemeinde/{id}", response_model=GemeindeRead)
async def update_gemeinde(
    id: int,
    obj_in: GemeindeUpdate,
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    return await crud_gemeinde.update(db=db, id=id, obj_in=obj_in)


@router.delete("/gemeinde/{id}", status_code=204)
async def delete_gemeinde(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    await crud_gemeinde.delete(db=db, id=id)


class UserAdminUpdate(BaseModel):
    rolle_id: Optional[int] = Field(None)
    gemeinde_id: Optional[int] = Field(None)
    is_superuser: Optional[bool] = Field(None)


@router.get("/user", response_model=List[UserRead])
async def get_all_users(
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    result = await db.execute(select(User))
    return list(result.scalars().all())


@router.delete("/user/{user_id}", status_code=204)
async def delete_user_by_admin(
    user_id: UUID,
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Benutzer nicht gefunden")
    await db.delete(user)
    await db.commit()


@router.patch("/user/{user_id}", response_model=UserRead)
async def update_user_by_admin(
    user_id: UUID,
    obj_in: UserAdminUpdate,
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Benutzer nicht gefunden")
    if obj_in.rolle_id is not None:
        user.rolle_id = obj_in.rolle_id
    if obj_in.gemeinde_id is not None:
        user.gemeinde_id = obj_in.gemeinde_id
    if obj_in.is_superuser is not None:
        user.is_superuser = obj_in.is_superuser
    await db.commit()
    await db.refresh(user)
    return user
