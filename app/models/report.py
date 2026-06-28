from sqlalchemy import Column, Integer, String, ForeignKey, Float, JSON
from app.database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    summary = Column(String, nullable=True)
    competitors = Column(JSON, nullable=True)
    features = Column(JSON, nullable=True)
    revenue_model = Column(String, nullable=True)
    risks = Column(JSON, nullable=True)
    roadmap = Column(JSON, nullable=True)
    success_score = Column(Float, nullable=True)
    