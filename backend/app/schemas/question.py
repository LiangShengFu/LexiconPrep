from datetime import datetime
from pydantic import BaseModel


class QuestionResponse(BaseModel):
    id: str
    type: str
    content: str
    options: list
    difficulty: int
    subject: str
    chapter: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class AnswerRequest(BaseModel):
    user_answer: list[str]
    time_spent: int = 0


class AnswerResponse(BaseModel):
    is_correct: bool
    correct_answer: list
    analysis: str | None = None
