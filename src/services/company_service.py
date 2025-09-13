from sqlalchemy.orm import Session
from ..repository import db
from .. import schemas


def create_company(database: Session, company: schemas.CompanyCreate):
  new_company = db.Company(name=company.name)
  database.add(new_company)
  database.commit()
  database.refresh(new_company)
  return new_company


def get_companies(database: Session, skip: int = 0, limit: int = 100):
  return database.query(db.Company).offset(skip).limit(limit).all()


def get_company(database: Session, company_id: int):
  return database.query(db.Company).filter(db.Company.id == company_id).first()


def update_company(database: Session, company_id: int, company: schemas.CompanyCreate):
  db_company = database.query(db.Company).filter(
    db.Company.id == company_id).first()
  if db_company is None:
    return None

  db_company.name = company.name
  database.commit()
  database.refresh(db_company)
  return db_company


def delete_company(database: Session, company_id: int):
  db_company = database.query(db.Company).filter(
    db.Company.id == company_id).first()
  if db_company is None:
    return None

  database.delete(db_company)
  database.commit()
  return db_company
