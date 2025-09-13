from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
  id: str
  role: str


class UserCreate(UserBase):
  password: str
  role: Optional[str] = "user"


class UserLogin(UserCreate):
  pass


class User(UserBase):
  class Config:
    from_attributes = True
