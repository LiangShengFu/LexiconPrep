from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import User
from app.api.deps import get_current_user
from app.schemas.user import UserResponse, UserUpdate, PasswordChange
from app.core.security import hash_password, verify_password

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)


@router.put("/me/password")
async def change_password(
    data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not verify_password(data.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="当前密码错误")
    if len(data.new_password) < 6:
        raise HTTPException(status_code=400, detail="新密码至少 6 位")
    current_user.password_hash = hash_password(data.new_password)
    await db.commit()
    return {"status": "success"}


@router.put("/me", response_model=UserResponse)
async def update_me(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if data.nickname is not None:
        current_user.nickname = data.nickname
    if data.avatar is not None:
        current_user.avatar = data.avatar
    await db.commit()
    await db.refresh(current_user)
    return UserResponse.model_validate(current_user)
