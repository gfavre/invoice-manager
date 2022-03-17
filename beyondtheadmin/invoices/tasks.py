# -*- coding: utf-8 -*-
from config import celery_app

from .models import Invoice


@celery_app.task()
def generate_pdf(invoice_id, version, content):
    """A pointless Celery task to demonstrate usage."""
    try:
        invoice = Invoice.objects.get(id=invoice_id)
        invoice.generate_pdf(content)
        # en cas de crash retryer
    except Invoice.DoesNotExist:
        return
