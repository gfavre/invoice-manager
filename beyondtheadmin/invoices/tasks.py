# -*- coding: utf-8 -*-
import logging

from django.core.mail import EmailMessage

from anymail.exceptions import AnymailError

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


@celery_app.task(bind=True, max_retries=17, soft_time_limit=30)
def send_invoice_email(self, invoice_id, subject, message):
    """Send an invoice email."""
    try:
        invoice = Invoice.objects.get(id=invoice_id)
    except Invoice.DoesNotExist:
        logger.warning(f"Invoice {invoice_id} does not exist")
        return

    bcc = []
    if invoice.company.bcc_email:
        bcc.append(invoice.company.bcc_email)
    reply_to = []
    if not invoice.company.override_default_from_email:
        reply_to.append(invoice.company.from_email)
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=invoice.company.invoice_from_email,
        to=[invoice.client.full_contact_email],
        reply_to=reply_to,
        bcc=bcc
    )
    if not invoice.latest_pdf:
        try:
            invoice.generate_latest_pdf()
        except Exception:
            self.retry(countdown=2 ** self.request.retries, exc=e)

    email.attach_file(invoice.latest_pdf.path, 'application/pdf')
    try:
        email.send()
        invoice.set_sent()
    except AnymailError as e:
        self.retry(countdown=2**self.request.retries, exc=e)
