from pydantic import BaseModel
from typing import List, Optional

class ReportOut(BaseModel):
    id: int
    project_id: int
    summary: Optional[str] = None
    competitors: Optional[List[str]] = None
    features: Optional[List[str]] = None
    revenue_model: Optional[str] = None
    risks: Optional[List[str]] = None
    roadmap: Optional[List[str]] = None
    success_score: Optional[float] = None

    class Config:
        from_attributes = True