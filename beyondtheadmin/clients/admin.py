from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_filter = ('client_type', )
    list_display = ('__str__', 'invoice_current_count')
