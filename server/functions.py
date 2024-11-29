import io
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from typing import Any, Dict
from fastapi import HTTPException
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from database import models, schemas

# Business logic

# factuur genereren

def generate_invoice(invoice_data):
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    table = Table(invoice_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(table)
    pdf.build(elements)
    pdf_content = buffer.getvalue()
    buffer.close()

    return pdf_content

# models

# company

def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Company).options(joinedload(models.Company.users)).offset(skip).limit(limit).all()

def get_company(db: Session, company_id: int):
    return db.query(models.Company).options(joinedload(models.Company.users)).filter(models.Company.id == company_id).first()

def create_company(db: Session, company: schemas.CompanyCreate):

    if not company.name:
        raise HTTPException(status_code=400, detail="Name field is required and cannot be null")
    
    companydb = models.Company()

    for var, value in vars(company).items():
        setattr(companydb, var, value) if value else None
    
    db.add(companydb)
    db.commit()   
    db.close()

    return companydb

def update_company(db: Session, company: schemas.CompanyCreate, company_id = int):

    if not company.name:
        raise HTTPException(status_code=400, detail="Name field is required and cannot be null")

    company_by_id: models.Company
    if (db.query(models.Company).filter(models.Company.id == company_id).first()):
        company_by_id = db.query(models.Company).filter(models.Company.id == company_id).first()

    for var, value in vars(company).items():
        setattr(company_by_id, var, value) if value else None
    
    db.add(company_by_id)
    db.commit()
    db.refresh(company_by_id)

    return company_by_id

def delete_company(db: Session, company_id: int):

    company_check = db.query(models.Company).filter(models.Company.id == company_id).first()
    if company_check is None:
        raise HTTPException(status_code=404, detail="Company with that ID was not found, so it cannot be deleted")

    db.query(models.Company).filter(models.Company.id == company_id).delete()
    db.commit()
    db.close()
    return f"Company with id: {company_id} has been deleted"

# invoice

def get_invoices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Invoice).options(joinedload(models.Invoice.remarks)).offset(skip).limit(limit).all()

def get_invoice(db: Session, invoice_id: int):
    return db.query(models.Invoice).options(joinedload(models.Invoice.remarks)).filter(models.Invoice.id == invoice_id).first()

def create_invoice(db: Session, invoice: schemas.InvoiceCreate):

    if not invoice.number:
        raise HTTPException(status_code=400, detail="number field is required and cannot be null")
    
    invoicedb = models.Invoice()

    for var, value in vars(invoice).items():
        setattr(invoicedb, var, value) if value else None
    
    db.add(invoicedb)
    db.commit()   
    db.close()

    return invoicedb

def update_invoice(db: Session, invoice: schemas.InvoiceCreate, invoice_id = int):

    if not invoice.number:
        raise HTTPException(status_code=400, detail="number field is required and cannot be null")

    invoice_by_id: models.Invoice
    if (db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()):
        invoice_by_id = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()

    for var, value in vars(invoice).items():
        setattr(invoice_by_id, var, value) if value else None
    
    db.add(invoice_by_id)
    db.commit()
    db.refresh(invoice_by_id)

    return invoice_by_id

def delete_invoice(db: Session, invoice_id: int):

    invoice_check = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if invoice_check is None:
        raise HTTPException(status_code=404, detail="Invoice with that ID was not found, so it cannot be deleted")

    db.query(models.Invoice).filter(models.Invoice.id == invoice_id).delete()
    db.commit()
    db.close()
    return f"Invoice with id: {invoice_id} has been deleted"

# user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).options(joinedload(models.User.invoices)).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).options(joinedload(models.User.invoices)).filter(models.User.id == user_id).first() 

def create_user(db: Session, user: schemas.UserCreate):

    if not user.username:
        raise HTTPException(status_code=400, detail="username field is required and cannot be null")

    userdb = models.User()

    for var, value in vars(user).items():
        setattr(userdb, var, value) if value else None
    
    db.add(userdb)
    db.commit()   
    db.close()

    return userdb

def update_user(db: Session, user: schemas.UserCreate, user_id = int):

    if not user.username:
        raise HTTPException(status_code=400, detail="username field is required and cannot be null")

    user_by_id: models.User
    if (db.query(models.User).filter(models.User.id == user_id).first()):
        user_by_id = db.query(models.User).filter(models.User.id == user_id).first()

    for var, value in vars(user).items():
        setattr(user_by_id, var, value) if value else None
    
    db.add(user_by_id)
    db.commit()
    db.refresh(user_by_id)

    return user_by_id

def delete_user(db: Session, user_id: int):

    user_check = db.query(models.User).filter(models.User.id == user_id).first()
    if user_check is None:
        raise HTTPException(status_code=404, detail="User with that ID was not found, so it cannot be deleted")

    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()
    db.close()
    return f"User with id: {user_id} has been deleted"

# profile

def get_profiles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Profile).options(joinedload(models.Profile.user)).offset(skip).limit(limit).all()

def get_profile(db: Session, profile_id: int):
    return db.query(models.Profile).options(joinedload(models.Profile.user)).filter(models.Profile.id == profile_id).first()

def create_profile(db: Session, profile: schemas.ProfileCreate):

    if not profile.firstname:
        raise HTTPException(status_code=400, detail="firstname field is required and cannot be null")
    
    profiledb = models.Profile()

    for var, value in vars(profile).items():
        setattr(profiledb, var, value) if value else None
    
    db.add(profiledb)
    db.commit()   
    db.close()

    return profiledb

def update_profile(db: Session, profile: schemas.ProfileCreate, profile_id = int):

    if not profile.firstname:
        raise HTTPException(status_code=400, detail="firstname field is required and cannot be null")

    profile_by_id: models.Profile
    if (db.query(models.Profile).filter(models.Profile.id == profile_id).first()):
        profile_by_id = db.query(models.Profile).filter(models.Profile.id == profile_id).first()

    for var, value in vars(profile).items():
        setattr(profile_by_id, var, value) if value else None
    
    db.add(profile_by_id)
    db.commit()
    db.refresh(profile_by_id)

    return profile_by_id

def delete_profile(db: Session, profile_id: int):

    profile_check = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    if profile_check is None:
        raise HTTPException(status_code=404, detail="Profile with that ID was not found, so it cannot be deleted")

    db.query(models.Profile).filter(models.Profile.id == profile_id).delete()
    db.commit()
    db.close()
    return f"Profile with id: {profile_id} has been deleted"

# remark

def get_remarks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Remark).options(joinedload(models.Remark.invoice)).offset(skip).limit(limit).all()

def get_remark(db: Session, remark_id: int):
    return db.query(models.Remark).options(joinedload(models.Remark.invoice)).filter(models.Remark.id == remark_id).first()

def create_remark(db: Session, remark: schemas.RemarkCreate):

    if not remark.description:
        raise HTTPException(status_code=400, detail="description field is required and cannot be null")
    
    remarkdb = models.Remark()

    for var, value in vars(remark).items():
        setattr(remarkdb, var, value) if value else None
    
    db.add(remarkdb)
    db.commit()   
    db.close()

    return remarkdb

def update_remark(db: Session, remark: schemas.RemarkCreate, remark_id = int):

    if not remark.description:
        raise HTTPException(status_code=400, detail="description field is required and cannot be null")

    remark_by_id: models.Remark
    if (db.query(models.Remark).filter(models.Remark.id == remark_id).first()):
        remark_by_id = db.query(models.Remark).filter(models.Remark.id == remark_id).first()

    for var, value in vars(remark).items():
        setattr(remark_by_id, var, value) if value else None
    
    db.add(remark_by_id)
    db.commit()
    db.refresh(remark_by_id)

    return remark_by_id

def delete_remark(db: Session, remark_id: int):

    remark_check = db.query(models.Remark).filter(models.Remark.id == remark_id).first()
    if remark_check is None:
        raise HTTPException(status_code=404, detail="Remark with that ID was not found, so it cannot be deleted")

    db.query(models.Remark).filter(models.Remark.id == remark_id).delete()
    db.commit()
    db.close()
    return f"Remark with id: {remark_id} has been deleted"