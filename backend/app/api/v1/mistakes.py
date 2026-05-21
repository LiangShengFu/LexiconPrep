from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.mistake import Mistake
from app.models.question import Question
from app.models.user import User
from app.api.deps import get_current_user
from app.schemas.mistake import MistakeResponse

router = APIRouter(prefix="/mistakes", tags=["mistakes"])


@router.get("", response_model=list[MistakeResponse])
async def list_mistakes(
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = (
        select(Mistake, Question.content, Question.subject)
        .join(Question, Mistake.question_id == Question.id)
        .where(Mistake.user_id == current_user.id)
        .order_by(Mistake.next_review_at.asc())
        .offset(offset).limit(limit)
    )
    result = await db.execute(q)
    rows = result.all()
    return [
        MistakeResponse(
            id=row[0].id,
            user_id=row[0].user_id,
            question_id=row[0].question_id,
            wrong_count=row[0].wrong_count,
            last_review_at=row[0].last_review_at,
            next_review_at=row[0].next_review_at,
            created_at=row[0].created_at,
            question_content=row[1],
            question_subject=row[2],
        )
        for row in rows
    ]


@router.delete("/{mistake_id}")
async def delete_mistake(
    mistake_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Mistake).where(Mistake.id == mistake_id, Mistake.user_id == current_user.id)
    )
    mistake = result.scalar_one_or_none()
    if not mistake:
        raise HTTPException(status_code=404, detail="Mistake not found")
    await db.delete(mistake)
    await db.commit()
    return {"status": "success"}


@router.post("/{mistake_id}/review")
async def review_mistake(
    mistake_id: str,
    remembered: bool = True,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Mistake).where(Mistake.id == mistake_id, Mistake.user_id == current_user.id)
    )
    mistake = result.scalar_one_or_none()
    if not mistake:
        raise HTTPException(status_code=404, detail="Mistake not found")

    mistake.last_review_at = datetime.utcnow()
    if remembered:
        intervals = [1, 3, 7, 14, 30, 60]
        idx = min(mistake.wrong_count, len(intervals) - 1)
        mistake.next_review_at = datetime.utcnow() + timedelta(days=intervals[idx])
    else:
        mistake.wrong_count += 1
        mistake.next_review_at = datetime.utcnow() + timedelta(days=1)

    await db.commit()
    return {"status": "success"}
