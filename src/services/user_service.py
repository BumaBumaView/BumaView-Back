from sqlalchemy.orm import Session
from ..repository import db
from .. import schemas


def create_user(database: Session, user: schemas.UserCreate):
  db_user = database.query(db.User).filter(db.User.id == user.id).first()
  if db_user:
    return None

  # In a real app, you'd hash the password
  new_user = db.User(id=user.id, role=user.role, password=user.password)
  database.add(new_user)
  database.commit()
  database.refresh(new_user)
  return new_user


def get_user(database: Session, user_id: str):
  return database.query(db.User).filter(db.User.id == user_id).first()


def get_users(database: Session, skip: int = 0, limit: int = 100):
  return database.query(db.User).offset(skip).limit(limit).all()


def update_user(database: Session, user_id: str, user: schemas.UserCreate):
  db_user = database.query(db.User).filter(db.User.id == user_id).first()
  if db_user is None:
    return None

  db_user.role = user.role
  db_user.password = user.password  # Again, hash in real life
  database.commit()
  database.refresh(db_user)
  return db_user


def delete_user(database: Session, user_id: str):
  db_user = database.query(db.User).filter(db.User.id == user_id).first()
  if db_user is None:
    return None

  database.delete(db_user)
  database.commit()
  return db_user
