from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.flashcard import Flashcard
from app.models.user import User
from app.api.deps import get_current_user
from app.schemas.flashcard import FlashcardCreate, FlashcardUpdate, FlashcardResponse

router = APIRouter(prefix="/flashcards", tags=["flashcards"])


@router.get("", response_model=list[FlashcardResponse])
async def list_flashcards(
    subject: str | None = None,
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = select(Flashcard).where(Flashcard.user_id == current_user.id)
    if subject:
        q = q.where(Flashcard.subject == subject)
    q = q.offset(offset).limit(limit)
    result = await db.execute(q)
    return [FlashcardResponse.model_validate(row) for row in result.scalars().all()]


@router.post("", response_model=FlashcardResponse, status_code=201)
async def create_flashcard(
    data: FlashcardCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    card = Flashcard(
        user_id=current_user.id,
        front=data.front,
        back=data.back,
        subject=data.subject,
        difficulty=data.difficulty,
        next_review_at=datetime.utcnow() + timedelta(days=1),
    )
    db.add(card)
    await db.commit()
    await db.refresh(card)
    return FlashcardResponse.model_validate(card)


@router.put("/{card_id}", response_model=FlashcardResponse)
async def update_flashcard(
    card_id: str,
    data: FlashcardUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Flashcard).where(Flashcard.id == card_id, Flashcard.user_id == current_user.id)
    )
    card = result.scalar_one_or_none()
    if not card:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    if data.front is not None:
        card.front = data.front
    if data.back is not None:
        card.back = data.back
    if data.difficulty is not None:
        card.difficulty = data.difficulty
    await db.commit()
    await db.refresh(card)
    return FlashcardResponse.model_validate(card)


@router.post("/{card_id}/review")
async def review_flashcard(
    card_id: str,
    remembered: bool = True,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Flashcard).where(Flashcard.id == card_id, Flashcard.user_id == current_user.id)
    )
    card = result.scalar_one_or_none()
    if not card:
        raise HTTPException(status_code=404, detail="Flashcard not found")

    card.review_count += 1
    if remembered:
        intervals = [1, 3, 7, 14, 30, 60]
        idx = min(card.review_count, len(intervals) - 1)
        card.next_review_at = datetime.utcnow() + timedelta(days=intervals[idx])
    else:
        card.next_review_at = datetime.utcnow() + timedelta(days=1)
    await db.commit()
    return {"status": "success"}


@router.delete("/{card_id}")
async def delete_flashcard(
    card_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Flashcard).where(Flashcard.id == card_id, Flashcard.user_id == current_user.id)
    )
    card = result.scalar_one_or_none()
    if not card:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    await db.delete(card)
    await db.commit()
    return {"status": "success"}
