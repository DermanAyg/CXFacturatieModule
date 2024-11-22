from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, BLOB
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import LargeBinary

Base = declarative_base()

class Company(Base):
    __tablename__ = "Company"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True)
    mobile = Column(Integer, unique=True, index=True, nullable=True)
    emergency_phone = Column(Integer, unique=True, index=True, nullable=True)
    kvk_nr = Column(String, unique=True, index=True, nullable=True)
    btw_nr = Column(String, unique=True, index=True, nullable=True)

    users = relationship("User", back_populates="company")

    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}', email='{self.email}', mobile={self.mobile}, emergency_phone={self.emergency_phone}, kvk_nr='{self.kvk_nr}', btw_nr='{self.btw_nr}')>"

class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=True)
    password = Column(String, unique=True, index=True, nullable=True)
    status = Column(String, index=True, nullable=True)
    last_activity = Column(String, index=True, nullable=True)
    created_at = Column(String, index=True, nullable=True)
    user_code = Column(String, index=True, nullable=True)
    role = Column(String, index=True, nullable=True)
    company_id = Column(Integer, ForeignKey("Company.id"), nullable=True)
    profile_id = Column(Integer, ForeignKey("Profile.id"), nullable=True)

    company = relationship("Company", back_populates="users")
    profile = relationship("Profile", back_populates="user", uselist=False)
    invoices = relationship("Invoice", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', status='{self.status}', last_activity='{self.last_activity}', created_at='{self.created_at}', user_code='{self.user_code}', role='{self.role}', company_id={self.company_id}, profile_id={self.profile_id})>"

class Profile(Base):
    __tablename__ = "Profile"

    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String, index=True, nullable=True)
    lastname = Column(String, index=True, nullable=True)
    phone = Column(String, unique=True, index=True, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True)
    date_of_birth = Column(String, index=True, nullable=True)
    gender = Column(String, index=True, nullable=True)
    address = Column(String, index=True, nullable=True)

    user = relationship("User", back_populates="profile")

    def __repr__(self):
        return f"<Profile(id={self.id}, firstname='{self.firstname}', lastname='{self.lastname}', phone='{self.phone}', email='{self.email}', date_of_birth='{self.date_of_birth}', gender='{self.gender}', address='{self.address}')>"

class Invoice(Base):
    __tablename__ = "Invoice"

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String, index=True, nullable=True)
    uploaded_at = Column(String, index=True, nullable=True)
    last_activity = Column(String, index=True, nullable=True)
    file = Column(LargeBinary, index=True, nullable=True)
    status = Column(String, index=True, nullable=True)
    user_id = Column(Integer, ForeignKey("User.id"))

    user = relationship("User", back_populates="invoices")
    remarks = relationship("Remark", back_populates="invoice")

    def __repr__(self):
        return f"<Invoice(id={self.id}, number='{self.number}', uploaded_at='{self.uploaded_at}', last_activity='{self.last_activity}', status='{self.status}', user_id={self.user_id})>"

class Remark(Base):
    __tablename__ = "Remark"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, index=True, nullable=True)
    created_at = Column(String, index=True, nullable=True)
    status = Column(String, index=True, nullable=True)
    invoice_id = Column(Integer, ForeignKey("Invoice.id"))

    invoice = relationship("Invoice", back_populates="remarks")

    def __repr__(self):
        return f"<Remark(id={self.id}, description='{self.description}', created_at='{self.created_at}', status='{self.status}', invoice_id={self.invoice_id})>"
