from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import Bank, Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ["name", "zip_code", "city"]
    list_display = ["name", "zip_code", "city", "get_users"]

    def get_queryset(self, request):
        return Company.all_objects.prefetch_related("users")

    def get_users(self, obj):
        def get_user_link(user):
            url = reverse("admin:users_user_change", args=[user.id])
            return mark_safe('<a href="{}">{}</a>'.format(url, str(user)))

        return mark_safe(", ".join([get_user_link(user) for user in obj.users.all()]))

    get_users.short_description = _("Users")


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    search_fields = ["name", "swift", "city"]
    list_display = ["name", "code", "swift", "city"]
