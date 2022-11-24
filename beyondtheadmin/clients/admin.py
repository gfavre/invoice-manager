from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("__str__", "invoice_current_count")
    list_filter = ("client_type",)
    search_fields = ("company_name", "zip_code", "city", "contact_first_name", "contact_last_name")
