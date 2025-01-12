from database import models, schemas
import os
import functions
from pytest_mock_resources import create_sqlite_fixture

pg = create_sqlite_fixture(models.Invoice, session=True)

def test_generate_invoice(pg):
    """
        Test the invoice generation function.
    """

    invoice_data = {
        "bedrijfsnaam": "Codelogix",
        "voornaam": "test4",
        "achternaam": "test4",
        "straat": "test4",
        "klant-naam": "test4",
        "klant-straat": "test4",
        "klant-huisnummer": "test4",
        "klant-postcode": "test4",
        "klant-plaats": "test4",
        "klant-kvk": "test4",
        "factuurnummer": "20241129",
        "factuurdatum": "",
        "vervaldatum": "",
        "btw-nummer": "",
        "user_id": "1",
        "producten": [
            {
            "hoeveelheid": "5",
            "omschrijving": "fdsfsdfsdf",
            "btw": "21",
            "prijs": "100"
            }
        ]
    }

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

    invoice_data = {
        "bedrijfsnaam": "Codelogix",
        "voornaam": "test4",
        "achternaam": "test4",
        "straat": "test4",
        "klant-naam": "test4",
        "klant-straat": "test4",
        "klant-huisnummer": "test4",
        "klant-postcode": "test4",
        "klant-plaats": "test4",
        "klant-kvk": "test4",
        "factuurnummer": "20241129",
        "factuurdatum": "",
        "vervaldatum": "",
        "btw-nummer": "",
        "user_id": "1",
        "producten": [
            {
                "hoeveelheid": "5",
                "omschrijving": "fdsfsdfsdf",
                "btw": "21",
                "prijs": "100"
            }
        ]
    }

    invoice_binary = functions.generate_invoice(invoice_data)

    functions.create_invoice(pg, models.Invoice(
        number="20241129",
        uploaded_at=None,
        last_activity=None,
        file=invoice_binary,
        status=None,
        user_id=None
    ))

    saved_invoice = functions.get_invoice(pg, 1)
    saved_invoice_file = schemas.InvoiceBase.decode_file(saved_invoice['file'])

    assert saved_invoice['number'] == "20241129"
    assert saved_invoice_file == invoice_binary

