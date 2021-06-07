from django.contrib import admin

from .models import Invoice, InvoiceLine


class InvoiceLineInline(admin.TabularInline):
    model = InvoiceLine


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    readonly_fields = ['status_changed', 'total']
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
        'qr_bill'
    )
    inlines = [InvoiceLineInline]
