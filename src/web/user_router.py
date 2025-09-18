from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..repository import db
from .. import schemas
from ..services import user_service

router = APIRouter()


@router.post("/users/", response_model=schemas.User)
def create_user_endpoint(user: schemas.UserCreate, database: Session = Depends(db.get_db)):
  db_user = user_service.create_user(database, user)
  if db_user is None:
    raise HTTPException(status_code=400, detail="User already registered")
  return db_user


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user_endpoint(user_id: str, database: Session = Depends(db.get_db)):
  db_user = user_service.get_user(database, user_id)
  if db_user is None:
    raise HTTPException(status_code=404, detail="User not found")
  return db_user


@router.get("/users/", response_model=List[schemas.User])
def read_users_endpoint(skip: int = 0, limit: int = 100, database: Session = Depends(db.get_db)):
  users = user_service.get_users(database, skip=skip, limit=limit)
  return users


@router.put("/users/{user_id}", response_model=schemas.User)
def update_user_endpoint(user_id: str, user: schemas.UserCreate, database: Session = Depends(db.get_db)):
  db_user = user_service.update_user(database, user_id, user)
  if db_user is None:
    raise HTTPException(status_code=404, detail="User not found")
  return db_user


@router.delete("/users/{user_id}", response_model=schemas.User)
def delete_user_endpoint(user_id: str, database: Session = Depends(db.get_db)):
  db_user = user_service.delete_user(database, user_id)
  if db_user is None:
    raise HTTPException(status_code=404, detail="User not found")
  return db_user
