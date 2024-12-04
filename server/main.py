import uvicorn

from sqlalchemy.orm import Session
from database import models, schemas
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from database.db import SessionLocal, engine
from typing import Any, Dict
from sqlalchemy import JSON, desc, update
from fastapi.responses import Response
import functions
import json

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ENDPOINTS

# Business logic

# Create invoice

@app.post("/generate-invoice/", status_code=status.HTTP_201_CREATED, tags=["Etc"])
def generate_invoice(data: Dict[str, Any], db: Session = Depends(get_db)):
    generated_invoice = functions.generate_invoice(data)

    functions.create_invoice(db, models.Invoice(
        number=data['factuurnummer'],
        uploaded_at=None,
        last_activity=None,
        file=generated_invoice,
        status="open",
        user_id=None
    ))

    return f"created invoice"

# Entities

# Company

@app.get("/company/", response_model=list[schemas.Company], tags=["company"])
def read_company(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    companies = functions.get_companies(db, skip=skip, limit=limit)
    return companies

@app.get("/company/{id}", response_model=schemas.Company, tags=["company"])
def read_company(company_id: int, db: Session = Depends(get_db)):
    company = functions.get_company(db, company_id)
    return company

@app.post("/company/", status_code=status.HTTP_201_CREATED, tags=["company"])
def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    company = functions.create_company(db, company)
    return f"created company"

@app.put("/company/", tags=["company"])
def edit_company(company_id: int, company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    form = functions.update_company(db, company, company_id)
    return f"Succesfully updated the company with id: {company_id}"

@app.delete("/company/{id}", tags=["company"])
def delete_company(company_id: int, db: Session = Depends(get_db)):
    functions.delete_company(db, company_id)
    return f"deleted company with id: {company_id}"

# Invoice

@app.get("/invoice/", response_model=list[schemas.Invoice], tags=["invoice"])
def read_invoice(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    invoices = functions.get_invoices(db, skip=skip, limit=limit)
    return invoices

@app.get("/invoice/{id}", response_model=schemas.Invoice, tags=["invoice"])
def read_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = functions.get_invoice(db, invoice_id)
    return invoice

@app.post("/invoice/", status_code=status.HTTP_201_CREATED, tags=["invoice"])
def create_invoice(invoice: schemas.InvoiceCreate, db: Session = Depends(get_db)):
    invoice = functions.create_invoice(db, invoice)
    return f"created invoice"

@app.put("/invoice/", tags=["invoice"])
def edit_invoice(invoice_id: int, invoice: schemas.InvoiceCreate, db: Session = Depends(get_db)):
    invoice = functions.update_invoice(db, invoice, invoice_id)
    return f"Succesfully updated the invoice with id: {invoice_id}"

@app.delete("/invoice/{id}", tags=["invoice"])
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    functions.delete_invoice(db, invoice_id)
    return f"deleted invoice with id: {invoice_id}"

# User

@app.get("/user/", response_model=list[schemas.User], tags=["user"])
def read_user(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = functions.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/user/{id}", response_model=schemas.User, tags=["user"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = functions.get_user(db, user_id)
    return user

@app.post("/user/", status_code=status.HTTP_201_CREATED, tags=["user"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user = functions.create_user(db, user)
    return f"created user"

@app.put("/user/", tags=["user"])
def edit_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    user = functions.update_user(db, user, user_id)
    return f"Succesfully updated the user with id: {user_id}"

@app.delete("/user/{id}", tags=["user"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    functions.delete_user(db, user_id)
    return f"deleted user with id: {user_id}"

# Remark

@app.get("/remark/", response_model=list[schemas.Remark], tags=["remark"])
def read_remark(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    remarks = functions.get_remarks(db, skip=skip, limit=limit)
    return remarks

@app.get("/remark/{id}", response_model=schemas.Remark, tags=["remark"])
def read_remark(remark_id: int, db: Session = Depends(get_db)):
    remark = functions.get_remark(db, remark_id)
    return remark

@app.post("/remark/", status_code=status.HTTP_201_CREATED, tags=["remark"])
def create_remark(remark: schemas.RemarkCreate, db: Session = Depends(get_db)):
    remark = functions.create_remark(db, remark)
    return f"created remark"

@app.put("/remark/", tags=["remark"])
def edit_remark(remark_id: int, remark: schemas.RemarkCreate, db: Session = Depends(get_db)):
    remark = functions.update_remark(db, remark, remark_id)
    return f"Succesfully updated the remark with id: {remark_id}"

@app.delete("/remark/{id}", tags=["remark"])
def delete_remark(remark_id: int, db: Session = Depends(get_db)):
    functions.delete_remark(db, remark_id)
    return f"deleted remark with id: {remark_id}"

# Profile

@app.get("/profile/", response_model=list[schemas.Profile], tags=["profile"])
def read_profile(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    profiles = functions.get_profiles(db, skip=skip, limit=limit)
    return profiles

@app.get("/profile/{id}", response_model=schemas.Profile, tags=["profile"])
def read_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = functions.get_profile(db, profile_id)
    return profile

@app.post("/profile/", status_code=status.HTTP_201_CREATED, tags=["profile"])
def create_profile(profile: schemas.ProfileCreate, db: Session = Depends(get_db)):
    profile = functions.create_profile(db, profile)
    return f"created profile"

@app.put("/profile/", tags=["profile"])
def edit_profile(profile_id: int, profile: schemas.ProfileCreate, db: Session = Depends(get_db)):
    profile = functions.update_profile(db, profile, profile_id)
    return f"Succesfully updated the profile with id: {profile_id}"

@app.delete("/profile/{id}", tags=["profile"])
def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    functions.delete_profile(db, profile_id)
    return f"deleted profile with id: {profile_id}"

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
