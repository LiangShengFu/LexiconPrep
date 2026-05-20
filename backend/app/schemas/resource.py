import uuid
from datetime import datetime
from pydantic import BaseModel


class ResourceResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None
    type: str
    file_url: str
    size: int
    subject: str
    year: int | None
    downloads: int
    created_at: datetime

    model_config = {"from_attributes": True}
