from database import models, schemas
import functions
from pytest_mock_resources import create_sqlite_fixture
from tests.fixtures import setup_single_test_invoice, setup_multiple_test_invoices

pg = create_sqlite_fixture(models.Invoice, session=True)

def test_empty_get_invoices(pg):
    assert len(functions.get_invoices(pg)) == 0

def test_not_empty_get_invoices(pg, setup_multiple_test_invoices):
    assert len(functions.get_invoices(pg)) == 2

def test_get_invoice_by_id(pg, setup_single_test_invoice):
    assert functions.get_invoice(pg, 1)['number'] == "12345"

def test_create_invoice(pg, setup_single_test_invoice):
    assert len(functions.get_invoices(pg)) == 1
    assert functions.get_invoice(pg, 1)['number'] == "12345"

def test_update_invoice(pg, setup_single_test_invoice):
    update_data = schemas.InvoiceCreate(
        number="111",
        uploaded_at=None,
        last_activity=None,
        file=None,
        status=None,
        user_id=None
    )
    assert functions.get_invoice(pg, 1)['number'] == "12345"
    updated_invoice = functions.update_invoice(pg, update_data, 1)
    assert updated_invoice.number == "111"

def test_delete_invoice(pg, setup_single_test_invoice):
    assert len(functions.get_invoices(pg)) == 1
    functions.delete_invoice(pg, 1)
    assert len(functions.get_invoices(pg)) == 0
