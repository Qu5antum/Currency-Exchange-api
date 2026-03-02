from pydantic import BaseModel, Field, EmailStr

class UserBase(BaseModel):
    username: str = Field(..., min_length=2, max_length=20)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True
