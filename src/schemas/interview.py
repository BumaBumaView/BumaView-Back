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

  def model_dump_json(self, *, indent=None, include=None, exclude=None, context=None, by_alias=None, exclude_unset=False, exclude_defaults=False, exclude_none=False, round_trip=False, warnings=True, fallback=None, serialize_as_any=False):
    return super().model_dump_json(indent=indent, include=include, exclude=exclude, context=context, by_alias=by_alias, exclude_unset=exclude_unset, exclude_defaults=exclude_defaults, exclude_none=exclude_none, round_trip=round_trip, warnings=warnings, fallback=fallback, serialize_as_any=serialize_as_any)

  class Config:
    from_attributes = True
