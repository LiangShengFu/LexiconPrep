"""Admin API — manage questions, users, and system."""
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.models.user import User
from app.models.question import Question
from app.models.study_log import StudyLog
from app.api.deps import get_admin_user
from app.core.utils import escape_search
from app.schemas.user import UserListResponse, UserRoleUpdate
from app.schemas.question import QuestionResponse, QuestionCreate, QuestionUpdate

router = APIRouter(prefix="/admin", tags=["admin"])


# ─── Questions CRUD ───

@router.get("/questions", response_model=list[QuestionResponse])
async def admin_list_questions(
    subject: str | None = Query(None),
    search: str | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    q = select(Question)
    if subject:
        q = q.where(Question.subject == subject)
    if search:
        q = q.where(Question.content.ilike(f"%{escape_search(search)}%"))
    q = q.order_by(Question.created_at.desc()).offset(offset).limit(limit)
    result = await db.execute(q)
    return [QuestionResponse.model_validate(row) for row in result.scalars().all()]


@router.post("/questions", response_model=QuestionResponse, status_code=201)
async def admin_create_question(
    data: QuestionCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    question = Question(**data.model_dump())
    db.add(question)
    await db.commit()
    await db.refresh(question)
    return QuestionResponse.model_validate(question)


@router.put("/questions/{question_id}", response_model=QuestionResponse)
async def admin_update_question(
    question_id: uuid.UUID,
    data: QuestionUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    result = await db.execute(select(Question).where(Question.id == question_id))
    question = result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="题目不存在")
    for key, val in data.model_dump(exclude_none=True).items():
        setattr(question, key, val)
    await db.commit()
    await db.refresh(question)
    return QuestionResponse.model_validate(question)


@router.delete("/questions/{question_id}")
async def admin_delete_question(
    question_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    result = await db.execute(select(Question).where(Question.id == question_id))
    question = result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="题目不存在")
    await db.delete(question)
    await db.commit()
    return {"status": "success"}


# ─── Users ───

@router.get("/users", response_model=list[UserListResponse])
async def admin_list_users(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    q = select(User).order_by(User.created_at.desc()).offset(offset).limit(limit)
    result = await db.execute(q)
    return [UserListResponse.model_validate(row) for row in result.scalars().all()]


@router.put("/users/{user_id}/role")
async def admin_update_user_role(
    user_id: uuid.UUID,
    data: UserRoleUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    user.role = data.role
    await db.commit()
    return {"status": "success"}


# ─── Stats ───

@router.get("/stats")
async def admin_stats(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    user_count = (await db.execute(select(func.count(User.id)))).scalar()
    question_count = (await db.execute(select(func.count(Question.id)))).scalar()
    answer_count = (await db.execute(select(func.count(StudyLog.id)))).scalar()

    subject_result = await db.execute(
        select(Question.subject, func.count(Question.id)).group_by(Question.subject)
    )
    subjects = {row[0]: row[1] for row in subject_result.all()}

    return {
        "users": user_count,
        "questions": question_count,
        "answers": answer_count,
        "subjects": subjects,
    }
