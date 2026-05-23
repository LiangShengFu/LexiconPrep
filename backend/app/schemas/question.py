import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class QuestionResponse(BaseModel):
    id: uuid.UUID
    type: str
    content: str
    options: list[str]
    answer: list[str]
    analysis: str | None = None
    difficulty: int
    subject: str
    chapter: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class QuestionCreate(BaseModel):
    type: str = "SINGLE"
    content: str = Field(..., max_length=2000)
    options: list[str]
    answer: list[str]
    analysis: str | None = Field(None, max_length=2000)
    difficulty: int = Field(default=1, ge=1, le=5)
    subject: str = Field(..., max_length=50)
    chapter: str | None = Field(None, max_length=100)


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
