from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from . import auth, schemas
from .repository import db
from .services import user_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")


def get_current_user(token: str = Depends(oauth2_scheme), database: Session = Depends(db.get_db)):
  credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials",
      headers={"WWW-Authenticate": "Bearer"},
  )
  try:
    payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
      raise credentials_exception
    # A bit of a hack, but works for now
    token_data = schemas.user.User(id=username, role="")
  except JWTError:
    raise credentials_exception
  user = user_service.get_user(database, user_id=token_data.id)
  if user is None:
    raise credentials_exception
  return user


def validate_env():
  import os
  required_vars = [
    "DIFY_INTERVIEW_QUESTION_GENERATION_API_KEY", "DIFY_ENDPOINT"]
  missing_vars = [var for var in required_vars if not os.getenv(var)]
  if missing_vars:
    raise EnvironmentError(
      f"Missing required environment variables: {', '.join(missing_vars)}")
