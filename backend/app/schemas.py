import datetime

from pydantic import BaseModel, EmailStr, ConfigDict

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ResumeBase(BaseModel):
    title: str
    content: str

class ResumeCreate(ResumeBase):
    pass

class Resume(ResumeBase):
    id: int
    owner_id: int
    model_config = ConfigDict(from_attributes=True)


class ResumeImprovementBase(BaseModel):
    original_content: str
    improved_content: str

class ResumeImprovement(ResumeImprovementBase):
    id: int
    resume_id: int
    created_at: datetime

    class Config:
        from_attributes = True