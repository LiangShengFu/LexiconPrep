import uuid
from datetime import datetime

from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class StudyLog(Base):
    __tablename__ = "study_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    question_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False)
    user_answer: Mapped[str] = mapped_column(String(500), nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    time_spent: Mapped[int] = mapped_column(Integer, default=0)
    timestamp: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
