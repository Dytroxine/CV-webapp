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