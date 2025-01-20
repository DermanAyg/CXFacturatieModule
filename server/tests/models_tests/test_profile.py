from database import models, schemas
import functions
from pytest_mock_resources import create_sqlite_fixture
from tests.fixtures import setup_single_test_profile, setup_multiple_test_profiles

pg = create_sqlite_fixture(models.Profile, session=True)

def test_empty_get_profiles(pg):
    assert len(functions.get_profiles(pg)) == 0

def test_not_empty_get_profiles(pg, setup_multiple_test_profiles):
    assert len(functions.get_profiles(pg)) == 2

def test_get_profile_by_id(pg, setup_single_test_profile):
    assert functions.get_profile(pg, 1).firstname == "test"

def test_create_profile(pg, setup_single_test_profile):
    assert len(functions.get_profiles(pg)) == 1
    assert functions.get_profile(pg, 1).firstname == "test"

def test_update_profile(pg, setup_single_test_profile):
    update_data = schemas.ProfileCreate(
        firstname="updated test",
        lastname=None,
        phone=None,
        email=None,
        date_of_birth=None,
        gender=None,
        address=None
    )
    assert functions.get_profile(pg, 1).firstname == "test"
    updated_profile = functions.update_profile(pg, update_data, 1)
    assert updated_profile.firstname == "updated test"

def test_delete_profile(pg, setup_single_test_profile):
    assert len(functions.get_profiles(pg)) == 1
    functions.delete_profile(pg, 1)
    assert len(functions.get_profiles(pg)) == 0