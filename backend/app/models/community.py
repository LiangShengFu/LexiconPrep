import uuid
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Text, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class CommunityPost(Base):
    __tablename__ = "community_posts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    subject: Mapped[str | None] = mapped_column(String(50), nullable=True)
    likes: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
