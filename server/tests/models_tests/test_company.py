from database import models, schemas
import functions
from pytest_mock_resources import create_sqlite_fixture
from tests.fixtures import setup_single_test_company, setup_multiple_test_companies

pg = create_sqlite_fixture(models.Company, session=True)

def test_empty_get_companies(pg):
    assert len(functions.get_companies(pg)) == 0

def test_not_empty_get_companies(pg, setup_multiple_test_companies):
    assert len(functions.get_companies(pg)) == 2

def test_get_company_by_id(pg, setup_single_test_company):
    assert functions.get_company(pg, 1).name == "test"

def test_create_company(pg, setup_single_test_company):
    assert len(functions.get_companies(pg)) == 1
    assert functions.get_company(pg, 1).name == "test"

def test_update_company(pg, setup_single_test_company):
    update_data = schemas.CompanyCreate(
        name="updated test",
        postcode=None,
        plaats=None,
        straat=None,
        huisnr=None,
        email=None,
        mobile=None,
        emergency_phone=None,
        kvk_nr=None,
        btw_nr=None,
        users=[]
    )
    assert functions.get_company(pg, 1).name == "test"
    updated_company = functions.update_company(pg, update_data, 1)
    assert updated_company.name == "updated test"

def test_delete_company(pg, setup_single_test_company):
    assert len(functions.get_companies(pg)) == 1
    functions.delete_company(pg, 1)
    assert len(functions.get_companies(pg)) == 0
