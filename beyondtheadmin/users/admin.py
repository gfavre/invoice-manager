from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from beyondtheadmin.users.forms import UserChangeForm, UserCreationForm


User = get_user_model()


class ClientInline(admin.TabularInline):
    model = User.clients.through
    raw_id_fields = ('client',)
    verbose_name = _("Clients")


class CompanyInline(admin.TabularInline):
    model = User.companies.through
    raw_id_fields = ('company',)


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        ("User", {
            "fields": ("name",)
        }),

    ) + tuple(auth_admin.UserAdmin.fieldsets)

    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]
    inlines = [ClientInline, CompanyInline]
