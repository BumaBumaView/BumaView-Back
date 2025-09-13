from sqlalchemy.orm import Session
from ..repository import db
from .. import schemas


def create_question(database: Session, question: schemas.QuestionCreate):
  new_question = db.Question(**question.dict())
  database.add(new_question)
  database.commit()
  database.refresh(new_question)
  return new_question


def get_questions(database: Session, skip: int = 0, limit: int = 100):
  return database.query(db.Question).offset(skip).limit(limit).all()


def get_question(database: Session, question_id: int):
  return database.query(db.Question).filter(db.Question.question_id == question_id).first()


def update_question(database: Session, question_id: int, question: schemas.QuestionCreate):
  db_question = database.query(db.Question).filter(
    db.Question.question_id == question_id).first()
  if db_question is None:
    return None

  for var, value in vars(question).items():
    setattr(db_question, var, value) if value else None

  database.commit()
  database.refresh(db_question)
  return db_question


def delete_question(database: Session, question_id: int):
  db_question = database.query(db.Question).filter(
    db.Question.question_id == question_id).first()
  if db_question is None:
    return None

  database.delete(db_question)
  database.commit()
  return db_question
