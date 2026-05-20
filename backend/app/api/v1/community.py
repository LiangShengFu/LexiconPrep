"""Community API — posts with real database persistence."""
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from app.core.database import get_db
from app.models.community import CommunityPost
from app.models.user import User
from app.models.study_log import StudyLog
from app.api.deps import get_current_user
from app.schemas.community import PostCreate, PostResponse

router = APIRouter(prefix="/community", tags=["community"])


@router.get("/posts", response_model=list[PostResponse])
async def list_posts(
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = (
        select(CommunityPost, User.nickname)
        .join(User, CommunityPost.user_id == User.id)
        .order_by(desc(CommunityPost.created_at))
        .offset(offset).limit(limit)
    )
    result = await db.execute(q)
    rows = result.all()
    return [
        PostResponse(
            id=row[0].id, user_id=row[0].user_id, content=row[0].content,
            subject=row[0].subject, likes=row[0].likes, created_at=row[0].created_at,
            user_nickname=row[1],
            user_avatar_letters=row[1][:2].upper() if row[1] else "??",
        )
        for row in rows
    ]


@router.post("/posts", response_model=PostResponse, status_code=201)
async def create_post(
    data: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = CommunityPost(user_id=current_user.id, content=data.content, subject=data.subject)
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return PostResponse(
        id=post.id, user_id=post.user_id, content=post.content,
        subject=post.subject, likes=post.likes, created_at=post.created_at,
        user_nickname=current_user.nickname,
        user_avatar_letters=current_user.nickname[:2].upper(),
    )


@router.post("/posts/{post_id}/like")
async def like_post(
    post_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(CommunityPost).where(CommunityPost.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="帖子不存在")
    post.likes += 1
    await db.commit()
    return {"likes": post.likes}


@router.delete("/posts/{post_id}")
async def delete_post(
    post_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(CommunityPost).where(CommunityPost.id == post_id, CommunityPost.user_id == current_user.id)
    )
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="帖子不存在或无权删除")
    await db.delete(post)
    await db.commit()
    return {"status": "success"}


@router.get("/leaderboard")
async def leaderboard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Top users by study log count in last 7 days
    from datetime import datetime, timedelta
    cutoff = datetime.utcnow() - timedelta(days=7)
    q = (
        select(User.nickname, func.count(StudyLog.id).label("cnt"))
        .join(StudyLog, StudyLog.user_id == User.id)
        .where(StudyLog.timestamp >= cutoff)
        .group_by(User.id, User.nickname)
        .order_by(desc("cnt"))
        .limit(5)
    )
    result = await db.execute(q)
    rows = result.all()
    if not rows:
        return [{"name": "暂无数据", "hours": 0}]
    return [{"name": row[0], "hours": row[1]} for row in rows]
