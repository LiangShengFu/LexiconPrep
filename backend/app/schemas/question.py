import uuid
from datetime import datetime
from pydantic import BaseModel


class QuestionResponse(BaseModel):
    id: uuid.UUID
    type: str
    content: str
    options: list[str]
    difficulty: int
    subject: str
    chapter: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class QuestionCreate(BaseModel):
    type: str = "SINGLE"
    content: str
    options: list[str]
    answer: list[str]
    analysis: str | None = None
    difficulty: int = 1
    subject: str
    chapter: str | None = None


class QuestionUpdate(BaseModel):
    type: str | None = None
    content: str | None = None
    options: list[str] | None = None
    answer: list[str] | None = None
    analysis: str | None = None
    difficulty: int | None = None
    subject: str | None = None
    chapter: str | None = None


class AnswerRequest(BaseModel):
    user_answer: list[str]
    time_spent: int = 0


class AnswerResponse(BaseModel):
    is_correct: bool
    correct_answer: list[str]
    analysis: str | None = None
