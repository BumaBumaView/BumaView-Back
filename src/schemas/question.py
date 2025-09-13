from pydantic import BaseModel
from typing import Optional


class QuestionBase(BaseModel):
  questions: str
  parent: Optional[int] = None
  company_id: int
  category: str
  question_at: int


class QuestionCreate(QuestionBase):
  pass


class Question(QuestionBase):
  question_id: int

  class Config:
    from_attributes = True
