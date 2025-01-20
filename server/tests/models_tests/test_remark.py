from database import models, schemas
import functions
from pytest_mock_resources import create_sqlite_fixture
from tests.fixtures import setup_single_test_remark, setup_multiple_test_remarks

pg = create_sqlite_fixture(models.Remark, session=True)

def test_empty_get_remarks(pg):
    assert len(functions.get_remarks(pg)) == 0

def test_not_empty_get_remarks(pg, setup_multiple_test_remarks):
    assert len(functions.get_remarks(pg)) == 2

def test_get_remark_by_id(pg, setup_single_test_remark):
    assert functions.get_remark(pg, 1).description == "test"

def test_create_remark(pg, setup_single_test_remark):
    assert len(functions.get_remarks(pg)) == 1
    assert functions.get_remark(pg, 1).description == "test"

def test_update_remark(pg, setup_single_test_remark):
    update_data = schemas.RemarkCreate(
        description="updated test",
        created_at=None,
        created_by=None,
        status=None,
        invoice_id=None
    )
    assert functions.get_remark(pg, 1).description == "test"
    updated_remark = functions.update_remark(pg, update_data, 1)
    assert updated_remark.description == "updated test"

def test_delete_remark(pg, setup_single_test_remark):
    assert len(functions.get_remarks(pg)) == 1
    functions.delete_remark(pg, 1)
    assert len(functions.get_remarks(pg)) == 0
