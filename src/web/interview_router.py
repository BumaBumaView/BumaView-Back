from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..repository import db
from .. import schemas
from ..services import interview_service, ai_service

router = APIRouter()


@router.post("/interviews/", response_model=schemas.Interview)
def create_interview_endpoint(interview: schemas.InterviewCreate, database: Session = Depends(db.get_db)):
  return interview_service.create_interview(database, interview)


@router.get("/interviews/", response_model=List[schemas.Interview])
def read_interviews_endpoint(skip: int = 0, limit: int = 100, database: Session = Depends(db.get_db)):
  return interview_service.get_interviews(database, skip=skip, limit=limit)


@router.get("/interviews/{interview_id}", response_model=schemas.Interview)
def read_interview_endpoint(interview_id: int, database: Session = Depends(db.get_db)):
  db_interview = interview_service.get_interview(database, interview_id)
  if db_interview is None:
    raise HTTPException(status_code=404, detail="Interview not found")
  return db_interview


@router.get("/interviews/{interview_id}/get-feedback")
def get_interview_feedback_endpoint(interview_id: int, database: Session = Depends(db.get_db)):
  feedback = ai_service.generate_feedback(interview_id)
  interview_service.save_feedback(database, interview_id, feedback)
  return {"feedback": feedback}


@router.put("/interviews/{interview_id}", response_model=schemas.Interview)
def update_interview_endpoint(interview_id: int, interview: schemas.InterviewCreate, database: Session = Depends(db.get_db)):
  db_interview = interview_service.update_interview(
    database, interview_id, interview)
  if db_interview is None:
    raise HTTPException(status_code=404, detail="Interview not found")
  return db_interview


@router.delete("/interviews/{interview_id}", response_model=schemas.Interview)
def delete_interview_endpoint(interview_id: int, database: Session = Depends(db.get_db)):
  db_interview = interview_service.delete_interview(database, interview_id)
  if db_interview is None:
    raise HTTPException(status_code=404, detail="Interview not found")
  return db_interview
