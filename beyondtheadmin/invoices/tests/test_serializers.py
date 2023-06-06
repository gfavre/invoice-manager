from django.test import RequestFactory, TestCase

from faker import Faker

from ..models import InvoiceLine
from ..serializers import InvoiceSerializer
from .factories import InvoiceFactory, InvoiceLineFactory


fake = Faker(locale="fr_CH")


class InvoiceSerializerTests(TestCase):
    def setUp(self) -> None:
        self.request = RequestFactory().get("/")
        self.context = {"request": self.request}
        self.invoice = InvoiceFactory()
        self.lines = InvoiceLineFactory.create_batch(3, invoice=self.invoice)
        self.data = {
            "due_date": "2023-07-01",
            "title": fake.sentence(),
            "lines": [
                {
                    "id": str(self.lines[0].id),
                    "quantity": fake.pydecimal(min_value=1, max_value=10, right_digits=2),
                    "price_per_unit": fake.pydecimal(min_value=50, max_value=300, right_digits=2),
                    "unit": "h",
                    "description": fake.text(),
                }
            ],
        }

    def test_update_wipes_missing_lines(self):
        serializer = InvoiceSerializer(
            instance=self.invoice, data=self.data, partial=True, context=self.context
        )
        serializer.is_valid()
        serializer.save()
        # Assert we only have one line
        self.assertEqual(InvoiceLine.objects.count(), 1)
        # Retrieve the updated line
        updated_line = InvoiceLine.objects.first()
        self.assertEqual(updated_line.id, self.lines[0].id)

    def test_update_invoice_data(self):
        serializer = InvoiceSerializer(
            instance=self.invoice, data=self.data, partial=True, context=self.context
        )
        serializer.is_valid()
        serializer.save()
        # Assert that the invoice has been updated correctly
        self.invoice.refresh_from_db()
        self.assertEqual(str(self.invoice.title), self.data["title"])

    def test_update_lines(self):
        serializer = InvoiceSerializer(
            instance=self.invoice, data=self.data, partial=True, context=self.context
        )
        serializer.is_valid()
        serializer.save()
        updated_line = InvoiceLine.objects.first()
        self.assertEqual(updated_line.quantity, self.data["lines"][0]["quantity"])
        self.assertEqual(updated_line.price_per_unit, self.data["lines"][0]["price_per_unit"])
        self.assertEqual(updated_line.description, self.data["lines"][0]["description"])

    def test_create_method(self):
        del self.data["lines"][0]["id"]
        # Create the serializer instance with no existing invoice
        serializer = InvoiceSerializer(data=self.data)
        serializer.is_valid()
        invoice = serializer.save()
        created_lines = InvoiceLine.objects.filter(invoice=invoice)
        # Assert that the lines have been created correctly
        self.assertEqual(created_lines.count(), 1)
