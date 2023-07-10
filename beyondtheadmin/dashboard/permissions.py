from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class HasCompanyMixin(UserPassesTestMixin):
    def test_func(self):
        # noinspection PyUnresolvedReferences
        return self.request.user.has_company

    def handle_no_permission(self):
        raise PermissionDenied
