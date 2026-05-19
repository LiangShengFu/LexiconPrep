from datetime import datetime
from pydantic import BaseModel


class FlashcardCreate(BaseModel):
    front: str
    back: str
    subject: str | None = None
    difficulty: int = 1


class FlashcardUpdate(BaseModel):
    front: str | None = None
    back: str | None = None
    difficulty: int | None = None


class FlashcardResponse(BaseModel):
    id: str
    user_id: str
    front: str
    back: str
    subject: str | None = None
    difficulty: int
    review_count: int
    next_review_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}
