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


class StudyPlanRequest(BaseModel):
    days: int = Field(default=7, ge=3, le=30, description="计划天数")
    daily_minutes: int = Field(default=60, ge=15, le=300, description="每日可用学习分钟数")
    target_subjects: list[str] | None = Field(None, description="重点攻克学科")


class DayPlan(BaseModel):
    day: int
    focus: str
    tasks: list[str]
    duration_minutes: int
    review_topics: list[str]


class StudyPlanResponse(BaseModel):
    plan: list[DayPlan]
    summary: str
    estimated_accuracy_gain: str
