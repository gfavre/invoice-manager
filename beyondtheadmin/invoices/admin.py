from django.contrib import admin

from .models import Invoice, InvoiceLine, InvoicePDF


class InvoiceLineInline(admin.TabularInline):
    model = InvoiceLine


class InvoicePDFInline(admin.TabularInline):
    model = InvoicePDF
    readonly_fields = ['pdf', 'version']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    fields = (
        ('status', 'status_changed'),
        ('company', 'client'),
        'code',
        'displayed_date',
        'due_date',
        'title',
        ('period_start', 'period_end'),
        'description',
        'vat_rate',
        'total',
        'qr_bill',
    )
    inlines = [InvoiceLineInline, InvoicePDFInline]
    list_display = ('code', 'company', 'client', 'total', 'displayed_date', 'status')
    list_filter = ('status', 'company', 'client')
    readonly_fields = ['status_changed', 'total']
    search_fields = ('code', 'company__name', 'client__company_name',
                     'client__contact_first_name', 'client__contact_last_name', 'total')
