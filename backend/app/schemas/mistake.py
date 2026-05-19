from datetime import datetime
from pydantic import BaseModel


class MistakeResponse(BaseModel):
    id: str
    user_id: str
    question_id: str
    wrong_count: int
    last_review_at: datetime | None
    next_review_at: datetime
    created_at: datetime
    question_content: str | None = None
    question_subject: str | None = None

    model_config = {"from_attributes": True}
