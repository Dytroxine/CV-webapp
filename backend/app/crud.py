from sqlalchemy.orm import Session
from . import models, schemas, security

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_resume(db: Session, resume_id: int, user_id: int):
    return db.query(models.Resume).filter(
        models.Resume.id == resume_id,
        models.Resume.owner_id == user_id
    ).first()


def get_user_resumes(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Resume).filter(
        models.Resume.owner_id == user_id
    ).offset(skip).limit(limit).all()


def create_resume(db: Session, resume: schemas.ResumeCreate, user_id: int):
    db_resume = models.Resume(
        title=resume.title,
        content=resume.content,
        owner_id=user_id
    )
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume


def update_resume(db: Session, resume_id: int, resume: schemas.ResumeCreate, user_id: int):
    db_resume = get_resume(db, resume_id, user_id)
    if db_resume:
        db_resume.title = resume.title
        db_resume.content = resume.content
        db.commit()
        db.refresh(db_resume)
    return db_resume


def delete_resume(db: Session, resume_id: int, user_id: int):
    db_resume = get_resume(db, resume_id, user_id)
    if db_resume:
        db.delete(db_resume)
        db.commit()
    return db_resume