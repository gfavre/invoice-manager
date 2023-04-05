from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Invoice, InvoiceLine, InvoicePDF


class InvoiceLineInline(admin.TabularInline):
    model = InvoiceLine


class InvoicePDFInline(admin.TabularInline):
    model = InvoicePDF
    readonly_fields = ["pdf", "version"]


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    fields = (
        ("status", "status_changed"),
        ("company", "client"),
        "code",
        "displayed_date",
        "due_date",
        "title",
        ("period_start", "period_end"),
        "description",
        "vat_rate",
        "total",
        "qr_bill",
    )
    inlines = [InvoiceLineInline, InvoicePDFInline]
    list_display = (
        "id",
        "code",
        "company",
        "client",
        "total",
        "displayed_date",
        "status",
        "user_link",
    )
    list_filter = ("status", "company", "client")
    raw_id_fields = ("company", "client")
    readonly_fields = ["status_changed", "total"]
    search_fields = (
        "code",
        "company__name",
        "client__company_name",
        "client__contact_first_name",
        "client__contact_last_name",
        "total",
        "id",
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("created_by", "company", "client")

    def user_link(self, obj):
        if not obj.created_by:
            return ""
        url = reverse("admin:users_user_change", args=[obj.created_by.id])
        return format_html('<a href="{}">{}</a>', url, obj.created_by)

    user_link.short_description = _("Created by")
    user_link.admin_order_field = "created_by__email"
