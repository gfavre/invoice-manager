from django.contrib import admin

from .models import Company, CompanyClient


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ['name', 'zip_code', 'city']


@admin.register(CompanyClient)
class CompanyClient(admin.ModelAdmin):
    list_display = ['company', 'client', 'invoice_current_count']
    list_filter = ['company']
    search_fields = ['company__name', 'client__name']
