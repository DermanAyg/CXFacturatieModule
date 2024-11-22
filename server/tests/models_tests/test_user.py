from database import models, schemas
import functions
from pytest_mock_resources import create_sqlite_fixture
from tests.fixtures import setup_single_test_user, setup_multiple_test_users

pg = create_sqlite_fixture(models.User, session=True)

def test_empty_get_users(pg):
    assert len(functions.get_users(pg)) == 0

def test_not_empty_get_users(pg, setup_multiple_test_users):
    assert len(functions.get_users(pg)) == 2

def test_get_user_by_id(pg, setup_single_test_user):
    assert functions.get_user(pg, 1).username == "test"

def test_create_user(pg, setup_single_test_user):
    assert len(functions.get_users(pg)) == 1
    assert functions.get_user(pg, 1).username == "test"

def test_update_user(pg, setup_single_test_user):
    update_data = schemas.UserCreate(
        username="updated test",
        password=None,
        status=None,
        last_activity=None,
        created_at=None,
        user_code=None,
        role=None,
        company_id=None,
        profile_id=None,
        invoices=[]
    )
    assert functions.get_user(pg, 1).username == "test"
    updated_user = functions.update_user(pg, update_data, 1)
    assert updated_user.username == "updated test"

def test_delete_user(pg, setup_single_test_user):
    assert len(functions.get_users(pg)) == 1
    functions.delete_user(pg, 1)
    assert len(functions.get_users(pg)) == 0
