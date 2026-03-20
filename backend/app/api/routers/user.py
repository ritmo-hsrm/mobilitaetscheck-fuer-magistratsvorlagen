from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.deps import current_active_user, current_superuser, get_async_session
from app.crud.user import crud_user as crud
from app.models.user import User
from app.schemas.user import UserRead as ReadSchema

router = APIRouter()


class MyGruppeUpdate(BaseModel):
    gruppe_id: Optional[int] = None


@router.patch("/me/gruppe", response_model=ReadSchema)
async def update_my_gruppe(
    obj_in: MyGruppeUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user),
):
    result = await db.execute(select(User).where(User.id == current_user.id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Benutzer nicht gefunden")
    user.gruppe_id = obj_in.gruppe_id
    await db.commit()
    await db.refresh(user)
    return user


@router.get(
    "",
    response_model=List[ReadSchema],
    dependencies=[Depends(current_superuser)],
)
async def get_all_users_in_municipality(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
):

    instances = await crud.get_all(
        db=db,
        gemeinde_id=user.gemeinde_id,
        sort_params=[("name", "asc")],
    )
    return instances
