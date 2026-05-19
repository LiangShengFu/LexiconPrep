from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.models.user import User
from app.api.deps import get_current_user

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/overview")
async def get_overview(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Return KPI data for the current user."""
    return {
        "streak_days": current_user.streak_days,
        "total_knowledge_points": current_user.total_knowledge_points,
        "total_questions_answered": 0,
        "average_accuracy": 0.0,
        "total_study_minutes": 0,
    }


@router.get("/progress")
async def get_progress(
    current_user: User = Depends(get_current_user),
):
    return {
        "weekly": [
            {"week": "第1周", "questions": 24},
            {"week": "第2周", "questions": 30},
            {"week": "第3周", "questions": 28},
            {"week": "第4周", "questions": 42},
            {"week": "第5周", "questions": 45},
            {"week": "第6周", "questions": 38},
            {"week": "第7周", "questions": 52},
            {"week": "第8周", "questions": 48},
            {"week": "第9周", "questions": 55},
            {"week": "第10周", "questions": 62},
        ],
        "subjects": {
            "政治": 180,
            "英语": 220,
            "数学": 140,
            "专业课一": 160,
            "专业课二": 120,
        },
    }


@router.get("/community")
async def get_community():
    return {
        "posts": [
            {"id": "1", "user": "陈林", "avatar": "CL", "subject": "计算机科学", "content": "刚刚达成 60 天连续打卡！悬浮番茄钟真的改变了我的学习节奏。", "time": "2 小时前", "likes": 24},
            {"id": "2", "user": "张悦", "avatar": "ZY", "subject": "法学硕士", "content": "有谁有民法部分的好的复习资料吗？案例分析题太密了。", "time": "5 小时前", "likes": 18},
            {"id": "3", "user": "刘伟", "avatar": "LW", "subject": "心理学专硕", "content": "完成了第一次模拟考试，正确率 78%。还有提升空间但感觉还不错。", "time": "8 小时前", "likes": 31},
            {"id": "4", "user": "王静", "avatar": "WJ", "subject": "英语", "content": "分享我的词汇闪卡集——5500 词带例句，希望对大家有帮助。", "time": "1 天前", "likes": 47},
        ],
        "groups": [
            {"name": "计算机学习组", "online": 12},
            {"name": "法学复习圈", "online": 8},
            {"name": "英语角", "online": 21},
        ],
        "leaderboard": [
            {"name": "小明", "hours": 62},
            {"name": "杨柳", "hours": 58},
            {"name": "赵文", "hours": 51},
        ],
    }


@router.get("/trend")
async def get_trend(
    current_user: User = Depends(get_current_user),
):
    return {
        "labels": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"],
        "values": [28, 35, 42, 30, 48, 55, 42],
    }
