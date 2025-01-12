import io
import json
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from typing import Any, Dict
from fastapi import HTTPException
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from fastapi.encoders import jsonable_encoder

from database import models, schemas

# Business logic

# factuur genereren

def generate_invoice(invoice_data):

    print("@@@@@@@@@@@@@@@@@@@@")
    print(invoice_data)

    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    PAGE_WIDTH, PAGE_HEIGHT = A4
    LEFT_MARGIN = 72
    RIGHT_MARGIN = 72
    AVAILABLE_WIDTH = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN

    colWidths = [
        0.20 * AVAILABLE_WIDTH,
        0.40 * AVAILABLE_WIDTH,
        0.15 * AVAILABLE_WIDTH,
        0.10 * AVAILABLE_WIDTH,
        0.20 * AVAILABLE_WIDTH,
    ]

    styles = getSampleStyleSheet()
    normal_style = styles['Normal']

    centered_normal_style = ParagraphStyle(
        'CenteredStyle',
        parent=normal_style,
        alignment=TA_CENTER
    )
    
    right_normal_style = ParagraphStyle(
        'RightStyle',
        parent=normal_style,
        alignment=TA_RIGHT
    )

    elements.append(Paragraph(f"DATUM: {invoice_data['factuurdatum']}", normal_style))
    elements.append(Paragraph(f"FACTUURNR: {invoice_data['factuurnummer']}", normal_style))

    elements.append(Paragraph(f"Aan:", right_normal_style))
    elements.append(Paragraph(f"<strong>{invoice_data['klant-naam']}</strong>", right_normal_style))
    elements.append(Paragraph(f"{invoice_data['klant-straat']}", right_normal_style))
    # elements.append(Paragraph(f"{invoice_data['klant-postcode']} {invoice_data['klant-plaats']}", right_normal_style))
   
    elements.append(Spacer(2, 30))

    elements.append(Paragraph(f"Van:", right_normal_style))
    elements.append(Paragraph(f"<strong>{invoice_data['bedrijfsnaam']}</strong>", right_normal_style))
    elements.append(Paragraph(f"{invoice_data['straat']}", right_normal_style))
    # elements.append(Paragraph(f"{invoice_data['postcode']} {invoice_data['plaats']}", right_normal_style))
   
    elements.append(Spacer(2, 50))

    elements.append(Paragraph(f"VERVALDATUM", normal_style))
    elements.append(Paragraph(f"{invoice_data['vervaldatum']}", normal_style))

    elements.append(Spacer(1, 12))

    table_data = [["Hoeveelheid", "Omschrijving", "Prijs", "Btw", "Regeltotaal"]]
    for product in invoice_data['producten']:
        table_data.append([
            product.get("hoeveelheid", ""),
            product.get("omschrijving", ""),
            product.get("prijs", ""),
            product.get("btw", ""),
            product.get("regeltotaal", int(product['hoeveelheid']) * int(product['prijs'])),
        ])

    table = Table(table_data, colWidths=colWidths)
    
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 12))

    totaal_excl_btw = 0
    btw_9 = 0
    btw_21 = 0

    for product in invoice_data['producten']:
        totaal_excl_btw += int(product['hoeveelheid']) * int(product['prijs'])

        if product['btw'] == "9":
            btw_9 += (int(product['hoeveelheid']) * int(product['prijs'])) * 0.09

        if product['btw'] == "21":
            btw_21 += (int(product['hoeveelheid']) * int(product['prijs'])) * 0.21

    table_data = [
        ["Totaal excl. BTW", round(totaal_excl_btw, 2)],
        ["BTW 9%", round(btw_9, 2)],
        ["BTW 21%", round(btw_21, 2)],
        ["Totaal incl. BTW", round(totaal_excl_btw + btw_9 + btw_21, 2)]
    ]

    summary_table = Table(table_data, colWidths=[100, 100])

    summary_table.setStyle(TableStyle([
        ('GRID', (1, 0), (1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))
    summary_table.hAlign = 'RIGHT'

    elements.append(summary_table)

    elements.append(Spacer(2, 80))

    elements.append(Paragraph(f"<strong>{invoice_data['bedrijfsnaam']}</strong>", centered_normal_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Verzoekt u vriendelijk om het bedrag uiterlijk over te maken voor de vervaldatum naar rekeningnummer: NL01KNAB01234652314 ten name van {invoice_data['bedrijfsnaam']} onder vermelding van bovenstaand factuurnummer", centered_normal_style))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"KVK 91256834356 | BTW NL001234524235B66 | IBAN NL01KNAB01234652314", centered_normal_style))

    pdf.build(elements)
    pdf_content = buffer.getvalue()
    buffer.close()

    with open("test_invoice.pdf", "wb") as f:
        f.write(pdf_content)

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
    invoices = db.query(models.Invoice).options(joinedload(models.Invoice.remarks)).offset(skip).limit(limit).all()

    for invoice in invoices:
        if invoice.file:
            invoice.file = schemas.InvoiceBase.encode_file(invoice.file)

    return jsonable_encoder(invoices)

def get_invoices_by_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    invoices = db.query(models.Invoice).options(joinedload(models.Invoice.remarks)).filter(models.Invoice.user_id == user_id).offset(skip).limit(limit).all()

    for invoice in invoices:
        if invoice.file:
            invoice.file = schemas.InvoiceBase.encode_file(invoice.file)

    return jsonable_encoder(invoices)

def get_invoice(db: Session, invoice_id: int):
    invoice = db.query(models.Invoice).options(joinedload(models.Invoice.remarks)).filter(models.Invoice.id == invoice_id).first()
        
    if invoice.file:
        invoice.file = schemas.InvoiceBase.encode_file(invoice.file)
    
    return jsonable_encoder(invoice)

def create_invoice(db: Session, invoice: schemas.InvoiceCreate):

    if not invoice.number:
        raise HTTPException(status_code=400, detail="number field is required and cannot be null")
    
    invoicedb = models.Invoice()

    for var, value in vars(invoice).items():
        setattr(invoicedb, var, value) if value else None
    
    db.add(invoicedb)
    db.commit()   
    db.close()

    return schemas.Invoice.model_construct(invoicedb)

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

def update_invoice_status(db: Session, status: str, invoice_id = int):
    
    if not status:
        raise HTTPException(status_code=400, detail="status field is required and cannot be null")
    
    print(status)
    print(invoice_id)
    
    invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()

    invoice.status = status
    
    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    return invoice

def update_invoice_file(db: Session, invoice_data, invoice_id = int):
    if not invoice_data:
        raise HTTPException(status_code=400, detail="invoic data is required and cannot be null")
    
    invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()

    invoice.file = generate_invoice(invoice_data)
    
    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    return invoice

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
    users = db.query(models.User).options(joinedload(models.User.invoices)).offset(skip).limit(limit).all()
    
    for user in users:
        for invoice in user.invoices:
            if invoice:
                invoice.file = schemas.InvoiceBase.encode_file(invoice.file)

    return users

def get_user(db: Session, user_id: int):
    user = db.query(models.User).options(joinedload(models.User.invoices)).filter(models.User.id == user_id).first()

    for invoice in user.invoices:
        if invoice:
            invoice.file = schemas.InvoiceBase.encode_file(invoice.file)

    jsonable_encoder(user.invoices)

    return user

def get_user_by_email(db: Session, user_email: str):
    user = db.query(models.User).options(joinedload(models.User.invoices)).filter(models.User.username == user_email).first()
    
    for invoice in user.invoices:
        if invoice:
            invoice.file = schemas.InvoiceBase.encode_file(invoice.file)

    jsonable_encoder(user.invoices)

    return user

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