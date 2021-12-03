from django.contrib import admin

from .models import Company, CompanyClient


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(CompanyClient)
class CompanyClient(admin.ModelAdmin):
    list_display = ['company', 'client', 'invoice_current_count']
