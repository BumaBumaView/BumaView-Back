from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..repository import db
from .. import schemas
from ..services import company_service

router = APIRouter()


@router.post("/companies/", response_model=schemas.Company)
def create_company_endpoint(company: schemas.CompanyCreate, database: Session = Depends(db.get_db)):
  return company_service.create_company(database, company)


@router.get("/companies/", response_model=List[schemas.Company])
def read_companies_endpoint(skip: int = 0, limit: int = 100, database: Session = Depends(db.get_db)):
  return company_service.get_companies(database, skip=skip, limit=limit)


@router.get("/companies/{company_id}", response_model=schemas.Company)
def read_company_endpoint(company_id: int, database: Session = Depends(db.get_db)):
  db_company = company_service.get_company(database, company_id)
  if db_company is None:
    raise HTTPException(status_code=404, detail="Company not found")
  return db_company


@router.put("/companies/{company_id}", response_model=schemas.Company)
def update_company_endpoint(company_id: int, company: schemas.CompanyCreate, database: Session = Depends(db.get_db)):
  db_company = company_service.update_company(database, company_id, company)
  if db_company is None:
    raise HTTPException(status_code=404, detail="Company not found")
  return db_company


@router.delete("/companies/{company_id}", response_model=schemas.Company)
def delete_company_endpoint(company_id: int, database: Session = Depends(db.get_db)):
  db_company = company_service.delete_company(database, company_id)
  if db_company is None:
    raise HTTPException(status_code=404, detail="Company not found")
  return db_company
