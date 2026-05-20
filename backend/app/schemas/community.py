import uuid
from datetime import datetime
from pydantic import BaseModel


class PostCreate(BaseModel):
    content: str
    subject: str | None = None


class PostResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    content: str
    subject: str | None = None
    likes: int
    created_at: datetime
    user_nickname: str | None = None
    user_avatar_letters: str | None = None

    model_config = {"from_attributes": True}
