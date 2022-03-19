# -*- coding: utf-8 -*-
import logging

from config import celery_app

from .models import Invoice
from .pdf import generate_pdf as generate_pdf_invoice


logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=17, soft_time_limit=20)
def generate_pdf(self, invoice_id,  version, content):
    """Generate latest PDF for invoice."""
    try:
        invoice = Invoice.objects.get(id=invoice_id)
        generated_pdf = generate_pdf_invoice(content)
        if generated_pdf is None:
            self.retry(countdown=2**self.request.retries)
        else:
            invoice.add_pdf(generated_pdf, version)
    except Invoice.DoesNotExist:
        return


@celery_app.task(bind=True, max_retries=17, soft_time_limit=20)
def send_invoice_email(self, invoice_id, subject, message):
    """Send an invoice email."""
    try:
        invoice = Invoice.objects.get(id=invoice_id)

    except Invoice.DoesNotExist:
        logger.warning(f"Invoice {invoice_id} does not exist")
        return
