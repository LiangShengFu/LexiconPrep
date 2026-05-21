"""Stats endpoints — single-query aggregation, no hardcoded values."""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, cast, Date

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
    total = await db.execute(select(func.count(StudyLog.id)).where(StudyLog.user_id == current_user.id))
    correct = await db.execute(select(func.count(StudyLog.id)).where(
        StudyLog.user_id == current_user.id, StudyLog.is_correct == True
    ))
    total_seconds = await db.execute(select(func.coalesce(func.sum(StudyLog.time_spent), 0)).where(
        StudyLog.user_id == current_user.id
    ))
    total_answered = total.scalar() or 0
    correct_count = correct.scalar() or 0
    return {
        "streak_days": current_user.streak_days,
        "total_knowledge_points": current_user.total_knowledge_points,
        "total_questions_answered": total_answered,
        "average_accuracy": round(correct_count / total_answered * 100, 1) if total_answered > 0 else 0.0,
        "total_study_minutes": (total_seconds.scalar() or 0) // 60,
    }


@router.get("/progress")
async def get_progress(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Single query: weekly question counts for last 10 weeks
    cutoff = datetime.utcnow() - timedelta(days=70)
    weeks_result = await db.execute(
        select(
            func.date_trunc('week', StudyLog.timestamp).label('week_start'),
            func.count(StudyLog.id)
        )
        .where(StudyLog.user_id == current_user.id, StudyLog.timestamp >= cutoff)
        .group_by('week_start')
        .order_by('week_start')
    )
    weeks_data = {str(row[0])[:10]: row[1] for row in weeks_result.all()}
    weekly = []
    for i in range(9, -1, -1):
        week_start = (datetime.utcnow() - timedelta(days=7 * (i + 1))).strftime('%Y-%m-%d')
        cnt = 0
        for wk, c in weeks_data.items():
            if wk >= week_start:
                cnt += c
                break
        weekly.append({"week": f"第{10 - i}周", "questions": cnt or 0})

    # Single query: subject distribution
    subject_result = await db.execute(
        select(Question.subject, func.count(StudyLog.id))
        .join(Question, StudyLog.question_id == Question.id)
        .where(StudyLog.user_id == current_user.id)
        .group_by(Question.subject)
    )
    subjects = {row[0]: row[1] for row in subject_result.all()} or {"暂无数据": 1}
    return {"weekly": weekly, "subjects": subjects}


@router.get("/trend")
async def get_trend(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    day_labels = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    cutoff = datetime.utcnow() - timedelta(days=7)
    # Single query: daily counts
    daily_result = await db.execute(
        select(
            cast(StudyLog.timestamp, Date).label('day'),
            func.count(StudyLog.id)
        )
        .where(StudyLog.user_id == current_user.id, StudyLog.timestamp >= cutoff)
        .group_by('day')
        .order_by('day')
    )
    daily_data = {str(row[0]): row[1] for row in daily_result.all()}
    values = []
    for day_offset in range(6, -1, -1):
        day = (datetime.utcnow() - timedelta(days=day_offset)).strftime('%Y-%m-%d')
        values.append(daily_data.get(day, 0))
    return {"labels": day_labels, "values": values}
