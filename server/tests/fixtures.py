import pytest
from database import models
import functions
import io

# user

@pytest.fixture
def setup_single_test_user(pg):
    functions.create_user(pg, models.User(
        username="test",
        password=None,
        status=None,
        last_activity=None,
        created_at=None,
        user_code=None,
        role=None,
        company_id=None,
        profile_id=None,
        invoices=[]
    ))

@pytest.fixture
def setup_multiple_test_users(pg):
    functions.create_user(pg, models.User(
        username="test1",
        password=None,
        status=None,
        last_activity=None,
        created_at=None,
        user_code=None,
        role=None,
        company_id=None,
        profile_id=None,
        invoices=[]
    ))
    functions.create_user(pg, models.User(
        username="test2",
        password=None,
        status=None,
        last_activity=None,
        created_at=None,
        user_code=None,
        role=None,
        company_id=None,
        profile_id=None,
        invoices=[]
    ))

# remark

@pytest.fixture
def setup_single_test_remark(pg):
    functions.create_remark(pg, models.Remark(
        description="test",
        created_at=None,
        status=None,
        invoice_id=None
    ))

@pytest.fixture
def setup_multiple_test_remarks(pg):
    functions.create_remark(pg, models.Remark(
        description="test1",
        created_at=None,
        status=None,
        invoice_id=None
    ))
    functions.create_remark(pg, models.Remark(
        description="test2",
        created_at=None,
        status=None,
        invoice_id=None
    ))

# profile

@pytest.fixture
def setup_single_test_profile(pg):
    functions.create_profile(pg, models.Profile(
        firstname="test",
        lastname=None,
        phone=None,
        email=None,
        date_of_birth=None,
        gender=None,
        address=None
    ))

@pytest.fixture
def setup_multiple_test_profiles(pg):
    functions.create_profile(pg, models.Profile(
        firstname="test",
        lastname=None,
        phone=None,
        email=None,
        date_of_birth=None,
        gender=None,
        address=None
    ))
    functions.create_profile(pg, models.Profile(
        firstname="test",
        lastname=None,
        phone=None,
        email=None,
        date_of_birth=None,
        gender=None,
        address=None
    ))

# invoice

@pytest.fixture
def setup_single_test_invoice(pg):
    functions.create_invoice(pg, models.Invoice(
        number="12345",
        uploaded_at=None,
        last_activity=None,
        file=None,
        status=None,
        user_id=None
    ))

@pytest.fixture
def setup_multiple_test_invoices(pg):
    functions.create_invoice(pg, models.Invoice(
        number="12345",
        uploaded_at=None,
        last_activity=None,
        file=None,
        status=None,
        user_id=None
    ))
    functions.create_invoice(pg, models.Invoice(
        number="123456",
        uploaded_at=None,
        last_activity=None,
        file=None,
        status=None,
        user_id=None
    ))

# company

@pytest.fixture
def setup_single_test_company(pg):
    functions.create_company(pg, models.Company(
        name="test",
        email=None,
        mobile=None,
        emergency_phone=None,
        kvk_nr=None,
        btw_nr=None
    ))

@pytest.fixture
def setup_multiple_test_companies(pg):
    functions.create_company(pg, models.Company(
        name="test1",
        email=None,
        mobile=None,
        emergency_phone=None,
        kvk_nr=None,
        btw_nr=None
    ))
    functions.create_company(pg, models.Company(
        name="test2",
        email=None,
        mobile=None,
        emergency_phone=None,
        kvk_nr=None,
        btw_nr=None
    ))