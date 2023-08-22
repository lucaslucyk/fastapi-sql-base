from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    username: Optional[str] = None


class UserCreate(UserBase):
    username: str


class UserUpdate(UserBase):
    pass


class UserInDB(UserBase):
    id: int

    class Config:
        from_attributes = True


class User(UserInDB):
    pass