from typing import Optional
from pydantic import BaseModel
import datetime


class InterviewBase(BaseModel):
  eye_score: float
  pose_score: float
  answer_score: float
  feedback: str
  data: str
  student_id: str


class InterviewCreate(InterviewBase):
  feedback: Optional[str] = ""
  pass


class Interview(InterviewBase):
  id: int
  interviewed_at: datetime.date

  class Config:
    from_attributes = True
