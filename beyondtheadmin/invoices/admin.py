from django.contrib import admin

from .models import Invoice, InvoiceLine


class InvoiceLineInline(admin.TabularInline):
    model = InvoiceLine


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
        'pdf', 'pdf_version'
    )
    inlines = [InvoiceLineInline]
    list_display = ('code', 'company', 'client', 'total', 'displayed_date', 'status')
    list_filter = ('status', 'company', 'client')
    readonly_fields = ['status_changed', 'total', 'pdf', 'pdf_version']
    search_fields = ('code', 'company__name', 'client__name', 'total')
