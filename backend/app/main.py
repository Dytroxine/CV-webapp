from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import auth, crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="CV WebApp", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.include_router(auth.router, prefix="/auth", tags=["auth"])


@app.get("/resumes/", response_model=list[schemas.Resume])
def read_resumes(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(auth.get_current_user)
):
    return crud.get_user_resumes(db, user_id=current_user.id, skip=skip, limit=limit)


@app.post("/resumes/", response_model=schemas.Resume)
def create_resume(
        resume: schemas.ResumeCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(auth.get_current_user)
):
    return crud.create_resume(db=db, resume=resume, user_id=current_user.id)


@app.get("/resumes/{resume_id}", response_model=schemas.Resume)
def read_resume(
        resume_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(auth.get_current_user)
):
    resume = crud.get_resume(db, resume_id=resume_id, user_id=current_user.id)
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume


@app.put("/resumes/{resume_id}", response_model=schemas.Resume)
def update_resume(
        resume_id: int,
        resume: schemas.ResumeCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(auth.get_current_user)
):
    db_resume = crud.update_resume(db, resume_id=resume_id, resume=resume, user_id=current_user.id)
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return db_resume


@app.delete("/resumes/{resume_id}")
def delete_resume(
        resume_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(auth.get_current_user)
):
    db_resume = crud.delete_resume(db, resume_id=resume_id, user_id=current_user.id)
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return {"message": "Resume deleted successfully"}


@app.post("/resumes/{resume_id}/improve")
def improve_resume(
        resume_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(auth.get_current_user)
):
    resume = crud.get_resume(db, resume_id=resume_id, user_id=current_user.id)
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")

    improved_content = resume.content + " [Improved]"


    return {"improved_content": improved_content}


@app.get("/resumes/{resume_id}/improvements", response_model=list[schemas.ResumeImprovement])
def get_resume_improvements(
        resume_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(auth.get_current_user)
):
    resume = crud.get_resume(db, resume_id=resume_id, user_id=current_user.id)
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")

    improvements = db.query(models.ResumeImprovement).filter(
        models.ResumeImprovement.resume_id == resume_id
    ).order_by(models.ResumeImprovement.created_at.desc()).all()

    return improvements


@app.get("/")
def read_root():
    return {"message": "CV WebApp API is running"}


@app.post("/resumes/{resume_id}/save-improvement")
def save_improvement(
        resume_id: int,
        improvement: schemas.ResumeImprovementCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(auth.get_current_user)
):
    resume = crud.get_resume(db, resume_id=resume_id, user_id=current_user.id)
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")

    db_improvement = models.ResumeImprovement(
        resume_id=resume_id,
        original_content=improvement.original_content,
        improved_content=improvement.improved_content
    )
    db.add(db_improvement)
    db.commit()
    db.refresh(db_improvement)

    return db_improvement


@app.delete("/improvements/{improvement_id}")
def delete_improvement(
        improvement_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(auth.get_current_user)
):

    improvement = db.query(models.ResumeImprovement).join(
        models.Resume, models.ResumeImprovement.resume_id == models.Resume.id
    ).filter(
        models.ResumeImprovement.id == improvement_id,
        models.Resume.owner_id == current_user.id
    ).first()

    if improvement is None:
        raise HTTPException(status_code=404, detail="Improvement not found")

    db.delete(improvement)
    db.commit()

    return {"message": "Improvement deleted successfully"}


@app.delete("/resumes/{resume_id}/improvements")
def delete_all_improvements(
        resume_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(auth.get_current_user)
):
    resume = crud.get_resume(db, resume_id=resume_id, user_id=current_user.id)
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")

    db.query(models.ResumeImprovement).filter(
        models.ResumeImprovement.resume_id == resume_id
    ).delete()

    db.commit()

    return {"message": "All improvements deleted successfully"}
