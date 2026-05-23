import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    nickname: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    nickname: str
    avatar: str | None = None
    role: str = "user"
    streak_days: int
    total_knowledge_points: int
    created_at: datetime

    model_config = {"from_attributes": True}


class UserListResponse(BaseModel):
    id: uuid.UUID
    email: str
    nickname: str
    avatar: str | None = None
    role: str
    streak_days: int
    total_knowledge_points: int
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: UserResponse


class UserUpdate(BaseModel):
    nickname: str | None = None
    avatar: str | None = None


class UserRoleUpdate(BaseModel):
    role: str


class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)

    @field_validator("new_password")
    @classmethod
    def password_complexity(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("密码必须包含至少一个大写字母")
        if not any(c.islower() for c in v):
            raise ValueError("密码必须包含至少一个小写字母")
        if not any(c.isdigit() for c in v):
            raise ValueError("密码必须包含至少一个数字")
        return v

