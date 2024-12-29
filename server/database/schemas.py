from pydantic import BaseModel # type: ignore
from typing import Union, List, Optional
import base64

class RemarkBase(BaseModel):
    description: Optional[str]
    created_at: Optional[str]
    status: Optional[str]
    invoice_id: Optional[int]

class RemarkCreate(RemarkBase):
    pass

class Remark(RemarkBase):
    id: int

    class Config:
        from_attributes = True

class InvoiceBase(BaseModel):
    number: Optional[str]
    uploaded_at: Optional[str]
    last_activity: Optional[str]
    status: Optional[str]
    user_id: Optional[int]
    remarks: List[Remark] = []
    file: Optional[str]

    @staticmethod
    def encode_file(file_data: Optional[bytes]) -> Optional[str]:
        if file_data:
            return base64.b64encode(file_data).decode('utf-8')
        return None

    @staticmethod
    def decode_file(file_data: Optional[str]) -> Optional[bytes]:
        if file_data:
            return base64.b64decode(file_data)
        return None

class InvoiceCreate(InvoiceBase):
    pass

class Invoice(InvoiceBase):
    id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: Optional[str]
    password: Optional[str]
    status: Optional[str]
    last_activity: Optional[str]
    created_at: Optional[str]
    user_code: Optional[str]
    role: Optional[str]
    company_id: Optional[int]
    profile_id: Optional[int]
    invoices: List[Invoice] = []

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class CompanyBase(BaseModel):
    name: Optional[str]
    postcode: Optional[str]
    plaats: Optional[str]
    straat: Optional[str]
    huisnr: Optional[str]
    email: Optional[str]
    mobile: Optional[str]
    emergency_phone: Optional[str]
    kvk_nr: Optional[str]
    btw_nr: Optional[str]
    users: List[User] = []

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int

    class Config:
        from_attributes = True

class ProfileBase(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    date_of_birth: Optional[str]
    gender: Optional[str]
    address: Optional[str]

class ProfileCreate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: int

    class Config:
        from_attributes = True
