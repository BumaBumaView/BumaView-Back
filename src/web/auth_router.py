from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from .. import auth, schemas
from ..services import user_service
from ..repository import db

router = APIRouter()


def get_db():
  database = db.SessionLocal()
  try:
    yield database
  finally:
    database.close()


@router.post("/register", response_model=schemas.user.User)
def register(user: schemas.user.UserCreate, database: Session = Depends(get_db)):
  hashed_password = auth.get_password_hash(user.password)
  user_create = schemas.user.UserCreate(
    id=user.id, role=user.role, password=hashed_password)
  db_user = user_service.create_user(database, user=user_create)
  if db_user is None:
    raise HTTPException(status_code=400, detail="Email already registered")
  return db_user


@router.post("/token")
def login_for_access_token(user_login: schemas.user.UserLogin, database: Session = Depends(get_db)):
  user = user_service.get_user(database, user_id=user_login.id)
  if not user or not auth.verify_password(user_login.password, user.password):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
  access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = auth.create_access_token(
      data={"sub": user.id, "role": user.role}, expires_delta=access_token_expires
  )
  return {"access_token": access_token, "token_type": "bearer"}
