from sqlalchemy.orm import Session
from ..repository import db
from .. import schemas


def create_interview(database: Session, interview: schemas.InterviewCreate):
  new_interview = db.Interview(**interview.dict())
  database.add(new_interview)
  database.commit()
  database.refresh(new_interview)
  return new_interview


def get_interviews(database: Session, skip: int = 0, limit: int = 100):
  return database.query(db.Interview).offset(skip).limit(limit).all()


def get_interview(database: Session, interview_id: int):
  return database.query(db.Interview).filter(db.Interview.id == interview_id).first()


def update_interview(database: Session, interview_id: int, interview: schemas.InterviewCreate):
  db_interview = database.query(db.Interview).filter(
    db.Interview.id == interview_id).first()
  if db_interview is None:
    return None

  for var, value in vars(interview).items():
    setattr(db_interview, var, value) if value else None

  database.commit()
  database.refresh(db_interview)
  return db_interview


def delete_interview(database: Session, interview_id: int):
  db_interview = database.query(db.Interview).filter(
    db.Interview.id == interview_id).first()
  if db_interview is None:
    return None

  database.delete(db_interview)
  database.commit()
  return db_interview


def save_feedback(database: Session, interview_id: int, interview_data, feedback: str):
  update_interview(database, interview_id,
                   schemas.InterviewCreate(eye_score=interview_data.eye_score, pose_score=interview_data.pose_score, answer_score=interview_data.answer_score, data=interview_data.data, student_id=interview_data.student_id, feedback=feedback))
