from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.utils import escape_search
from app.models.resource import Resource
from app.models.user import User
from app.api.deps import get_current_user
from app.schemas.resource import ResourceResponse

router = APIRouter(prefix="/resources", tags=["resources"])


@router.get("", response_model=list[ResourceResponse])
async def list_resources(
    subject: str | None = Query(None),
    type: str | None = Query(None),
    search: str | None = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = select(Resource)
    if subject:
        q = q.where(Resource.subject == subject)
    if type:
        q = q.where(Resource.type == type)
    if search:
        q = q.where(Resource.title.ilike(f"%{escape_search(search)}%"))
    q = q.offset(offset).limit(limit)
    result = await db.execute(q)
    return [ResourceResponse.model_validate(row) for row in result.scalars().all()]


@router.get("/{resource_id}", response_model=ResourceResponse)
async def get_resource(
    resource_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Resource).where(Resource.id == resource_id))
    resource = result.scalar_one_or_none()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return ResourceResponse.model_validate(resource)
