from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectOut
from app.auth.dependencies import get_current_user
from app.models.report import Report
from app.schemas.report import ReportOut
from app.services.llm_service import analyze_startup_idea
from app.services.ml_service import predict_success_score

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=ProjectOut)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_project = Project(
        user_id=current_user.id,
        title=project.title,
        description=project.description,
        industry=project.industry
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


@router.get("/", response_model=list[ProjectOut])
def get_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Project).filter(Project.user_id == current_user.id).all()


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully"}
@router.post("/{project_id}/analyze", response_model=ReportOut)
@router.post("/{project_id}/analyze", response_model=ReportOut)
def analyze_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    result = analyze_startup_idea(
        title=project.title,
        description=project.description,
        industry=project.industry
    )

    ml_score = predict_success_score(
        industry=project.industry or "AI",
        description_length=len(project.description),
        competitor_count=len(result.get("competitors", [])),
        feature_count=len(result.get("features", [])),
        risk_count=len(result.get("risks", []))
    )

    new_report = Report(
        project_id=project.id,
        summary=result.get("summary"),
        competitors=result.get("competitors"),
        features=result.get("features"),
        revenue_model=result.get("revenue_model"),
        risks=result.get("risks"),
        roadmap=result.get("roadmap"),
        success_score=ml_score
    )

    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    return new_report

@router.get("/{project_id}/report", response_model=ReportOut)
def get_report(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    report = db.query(Report).filter(Report.project_id == project_id).first()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found. Run /analyze first.")

    return report