from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProjectCreate(BaseModel):
    title: str
    description: str
    industry: Optional[str] = None

class ProjectOut(BaseModel):
    id: int
    title: str
    description: str
    industry: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True