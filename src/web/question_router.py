from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..repository import db
from .. import schemas
from ..services import question_service

router = APIRouter()


def get_db():
  database = db.SessionLocal()
  try:
    yield database
  finally:
    database.close()


@router.post("/questions/", response_model=schemas.Question)
def create_question_endpoint(question: schemas.QuestionCreate, database: Session = Depends(get_db)):
  return question_service.create_question(database, question)


@router.get("/questions/", response_model=List[schemas.Question])
def read_questions_endpoint(skip: int = 0, limit: int = 100, database: Session = Depends(get_db)):
  return question_service.get_questions(database, skip=skip, limit=limit)


@router.get("/questions/{question_id}", response_model=schemas.Question)
def read_question_endpoint(question_id: int, database: Session = Depends(get_db)):
  db_question = question_service.get_question(database, question_id)
  if db_question is None:
    raise HTTPException(status_code=404, detail="Question not found")
  return db_question


@router.put("/questions/{question_id}", response_model=schemas.Question)
def update_question_endpoint(question_id: int, question: schemas.QuestionCreate, database: Session = Depends(get_db)):
  db_question = question_service.update_question(
    database, question_id, question)
  if db_question is None:
    raise HTTPException(status_code=404, detail="Question not found")
  return db_question


@router.delete("/questions/{question_id}", response_model=schemas.Question)
def delete_question_endpoint(question_id: int, database: Session = Depends(get_db)):
  db_question = question_service.delete_question(database, question_id)
  if db_question is None:
    raise HTTPException(status_code=404, detail="Question not found")
  return db_question
