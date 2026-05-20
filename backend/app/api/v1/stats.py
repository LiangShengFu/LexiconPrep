"""Stats endpoints — all data queried from the database, no hardcoded values."""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.models.user import User
from app.models.study_log import StudyLog
from app.models.question import Question
from app.api.deps import get_current_user

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/overview")
async def get_overview(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Total questions answered
    total_result = await db.execute(
        select(func.count(StudyLog.id)).where(StudyLog.user_id == current_user.id)
    )
    total_answered = total_result.scalar() or 0

    # Accuracy
    correct_result = await db.execute(
        select(func.count(StudyLog.id))
        .where(StudyLog.user_id == current_user.id, StudyLog.is_correct == True)
    )
    correct_count = correct_result.scalar() or 0

    # Focus minutes (sum of time_spent)
    time_result = await db.execute(
        select(func.coalesce(func.sum(StudyLog.time_spent), 0))
        .where(StudyLog.user_id == current_user.id)
    )
    total_seconds = time_result.scalar() or 0

    return {
        "streak_days": current_user.streak_days,
        "total_knowledge_points": current_user.total_knowledge_points,
        "total_questions_answered": total_answered,
        "average_accuracy": round(correct_count / total_answered * 100, 1) if total_answered > 0 else 0.0,
        "total_study_minutes": total_seconds // 60,
    }


@router.get("/progress")
async def get_progress(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Last 10 weeks of question counts
    weekly = []
    for week_offset in range(9, -1, -1):
        start = datetime.utcnow() - timedelta(days=7 * (week_offset + 1))
        end = datetime.utcnow() - timedelta(days=7 * week_offset)
        result = await db.execute(
            select(func.count(StudyLog.id)).where(
                StudyLog.user_id == current_user.id,
                StudyLog.timestamp >= start,
                StudyLog.timestamp < end,
            )
        )
        weekly.append({"week": f"第{10 - week_offset}周", "questions": result.scalar() or 0})

    # Subject distribution (last 30 days)
    cutoff = datetime.utcnow() - timedelta(days=30)
    subject_result = await db.execute(
        select(Question.subject, func.count(StudyLog.id))
        .join(Question, StudyLog.question_id == Question.id)
        .where(StudyLog.user_id == current_user.id, StudyLog.timestamp >= cutoff)
        .group_by(Question.subject)
    )
    subjects = {row[0]: row[1] for row in subject_result.all()}
    if not subjects:
        subjects = {"暂无数据": 1}

    return {"weekly": weekly, "subjects": subjects}


@router.get("/trend")
async def get_trend(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    day_labels = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    values = []

    for day_offset in range(6, -1, -1):
        day = datetime.utcnow() - timedelta(days=day_offset)
        start = day.replace(hour=0, minute=0, second=0)
        end = day.replace(hour=23, minute=59, second=59)
        result = await db.execute(
            select(func.count(StudyLog.id)).where(
                StudyLog.user_id == current_user.id,
                StudyLog.timestamp >= start,
                StudyLog.timestamp <= end,
            )
        )
        values.append(result.scalar() or 0)

    return {"labels": day_labels, "values": values}

