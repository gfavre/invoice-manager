# -*- coding: utf-8 -*-
from config import celery_app

from .models import Invoice
from .pdf import generate_pdf as generate_pdf_invoice


@celery_app.task(bind=True, max_retries=17, soft_time_limit=20)
def generate_pdf(self, invoice_id,  version, content):
    """A pointless Celery task to demonstrate usage."""
    try:
        invoice = Invoice.objects.get(id=invoice_id)
        generated_pdf = generate_pdf_invoice(content)
        if generated_pdf is None:
            self.retry(countdown=2**self.request.retries)
        else:
            invoice.add_pdf(generated_pdf, version)
    except Invoice.DoesNotExist:
        return
