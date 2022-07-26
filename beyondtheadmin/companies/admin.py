from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import Company, CompanyClient


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ['name', 'zip_code', 'city']
    list_display = ['name', 'zip_code', 'city', 'get_users']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('users')

    def get_users(self, obj):
        def get_user_link(user):
            url = reverse('admin:users_user_change', args=[user.id])
            return mark_safe('<a href="{}">{}</a>'.format(
                url, str(user)
            ))
        return mark_safe(', '.join([get_user_link(user) for user in obj.users.all()]))
    get_users.short_description = _('Users')


@admin.register(CompanyClient)
class CompanyClient(admin.ModelAdmin):
    list_display = ['company', 'client', 'invoice_current_count']
    list_filter = ['company']
    raw_id_fields = ('company', 'client')
    search_fields = ['company__name', 'client__company_name',
                     'client__contact_first_name', 'client__contact_last_name']
