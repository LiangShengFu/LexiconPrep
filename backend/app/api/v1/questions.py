from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.question import Question
from app.models.mistake import Mistake
from app.models.study_log import StudyLog
from app.models.user import User
from app.api.deps import get_current_user
from app.schemas.question import QuestionResponse, AnswerRequest, AnswerResponse

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("", response_model=list[QuestionResponse])
async def list_questions(
    subject: str | None = Query(None),
    difficulty: int | None = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = select(Question)
    if subject:
        q = q.where(Question.subject == subject)
    if difficulty:
        q = q.where(Question.difficulty == difficulty)
    q = q.offset(offset).limit(limit)
    result = await db.execute(q)
    return [QuestionResponse.model_validate(row) for row in result.scalars().all()]


@router.get("/{question_id}", response_model=QuestionResponse)
async def get_question(
    question_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Question).where(Question.id == question_id))
    question = result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return QuestionResponse.model_validate(question)


@router.post("/{question_id}/answer", response_model=AnswerResponse)
async def submit_answer(
    question_id: str,
    data: AnswerRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Question).where(Question.id == question_id))
    question = result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    answer_str = ",".join(sorted(data.user_answer)) if data.user_answer else ""
    correct_str = ",".join(sorted(question.answer)) if question.answer else ""
    is_correct = answer_str == correct_str

    # Write study log
    log = StudyLog(
        user_id=current_user.id,
        question_id=question_id,
        user_answer=answer_str,
        is_correct=is_correct,
        time_spent=data.time_spent,
    )
    db.add(log)

    # Update user stats
    current_user.total_knowledge_points = (current_user.total_knowledge_points or 0) + (1 if is_correct else 0)

    # Auto-capture mistake
    if not is_correct:
        existing = await db.execute(
            select(Mistake).where(Mistake.user_id == current_user.id, Mistake.question_id == question_id)
        )
        mistake = existing.scalar_one_or_none()
        if mistake:
            mistake.wrong_count += 1
            mistake.last_review_at = datetime.utcnow()
            intervals = [1, 3, 7, 14, 30]
            days = intervals[min(mistake.wrong_count - 1, len(intervals) - 1)]
            mistake.next_review_at = datetime.utcnow() + timedelta(days=days)
        else:
            mistake = Mistake(
                user_id=current_user.id,
                question_id=question_id,
                wrong_count=1,
                next_review_at=datetime.utcnow() + timedelta(days=1),
            )
            db.add(mistake)

    await db.commit()
    return AnswerResponse(
        is_correct=is_correct,
        correct_answer=question.answer,
        analysis=question.analysis if not is_correct else None,
    )
