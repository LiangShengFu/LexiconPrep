from pydantic import BaseModel, Field


class GenerateQuestionsRequest(BaseModel):
    subject: str = Field(..., max_length=50)
    chapter: str | None = Field(None, max_length=100)
    difficulty: int = Field(default=2, ge=1, le=5)
    count: int = Field(default=5, ge=1, le=20)
    type: str = Field(default="SINGLE", pattern="^(SINGLE|MULTIPLE)$")


class GeneratedQuestion(BaseModel):
    type: str
    content: str
    options: list[str]
    answer: list[str]
    analysis: str | None = None
    difficulty: int
    subject: str
    chapter: str | None = None


class GenerateQuestionsResponse(BaseModel):
    generated: int
    questions: list[GeneratedQuestion]


class DiagnosisResponse(BaseModel):
    diagnosis: str
