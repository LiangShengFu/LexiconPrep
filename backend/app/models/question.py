import uuid
from datetime import datetime

from sqlalchemy import String, Integer, DateTime, Text, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    options: Mapped[dict] = mapped_column(JSONB, nullable=False)
    answer: Mapped[dict] = mapped_column(JSONB, nullable=False)
    analysis: Mapped[str | None] = mapped_column(Text, nullable=True)
    difficulty: Mapped[int] = mapped_column(Integer, default=1)
    subject: Mapped[str] = mapped_column(String(50), nullable=False)
    chapter: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
