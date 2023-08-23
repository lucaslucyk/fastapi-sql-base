from datetime import datetime
from typing import Optional
from pydantic import UUID1, BaseModel, EmailStr, SecretStr, Field


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    email: Optional[EmailStr]
    password: Optional[str]


class UserInDBBase(UserBase):
    id: int
    uid: UUID1
    token: str
    is_active: bool
    is_staff: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserInDB(UserInDBBase):
    hashed_password: str


class User(UserInDBBase):
    ...


class UserActivate(BaseModel):
    uid: UUID1
    token: str