from database import models
import os
import functions
from pytest_mock_resources import create_sqlite_fixture

pg = create_sqlite_fixture(models.Invoice, session=True)

def test_generate_invoice(pg):
    """
        Test the invoice generation function.
    """

    invoice_data = [
        ["Hoeveelheid", "Beschrijving", "Prijs per eenheid", "Regeltotaal"],
        ["10", "Voorbeeld beschrijving werkzaamheden", "50.00", "500.00"],
        ["8", "Voorbeeld beschrijving werkzaamheden", "50.00", "400.00"],
        ["12", "Voorbeeld beschrijving werkzaamheden", "50.00", "600.00"],
        ["", "", "", ""],
        ["", "", "Subtotaal:", "1500.00"],
        ["", "", "BTW:", "315.00"],
        ["", "", "Subtotaal:", "1815.00"]
    ]

    invoice_binary = functions.generate_invoice(invoice_data)

    functions.create_invoice(pg, models.Invoice(
        number="20241129",
        uploaded_at=None,
        last_activity=None,
        file=invoice_binary,
        status=None,
        user_id=None
    ))

    assert invoice_binary is not None
    assert len(invoice_binary) > 0

def test_save_invoice(pg):
    """
    Test the saving of the invoice to the database containing the generated invoice pdf file.
    """

    invoice_data = [
        ["Hoeveelheid", "Beschrijving", "Prijs per eenheid", "Regeltotaal"],
        ["10", "Voorbeeld beschrijving werkzaamheden", "50.00", "500.00"],
        ["8", "Voorbeeld beschrijving werkzaamheden", "50.00", "400.00"],
        ["12", "Voorbeeld beschrijving werkzaamheden", "50.00", "600.00"],
        ["", "", "", ""],
        ["", "", "Subtotaal:", "1500.00"],
        ["", "", "BTW:", "315.00"],
        ["", "", "Subtotaal:", "1815.00"]
    ]

    invoice_binary = functions.generate_invoice(invoice_data)

    functions.create_invoice(pg, models.Invoice(
        number="20241129",
        uploaded_at=None,
        last_activity=None,
        file=invoice_binary,
        status=None,
        user_id=None
    ))

    assert functions.get_invoice(pg, 1).number == "20241129"
    assert functions.get_invoice(pg, 1).file == invoice_binary
