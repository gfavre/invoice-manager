from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from beyondtheadmin.companies.tests.factories import CompanyFactory
from beyondtheadmin.users.tests.factories import UserFactory

from ..views.dashboard import ClientAppView
from .factories import ClientFactory


class ClientAppViewTests(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = UserFactory()
        self.company = CompanyFactory()
        self.client = ClientFactory(company=self.company)
        self.user.companies.add(self.company)
        self.url = reverse("clients:update", kwargs={"pk": self.client.id})
        self.request = self._get_request(self.url)
        self.request.user = self.user
        self.view = ClientAppView.as_view()

    def _get_request(self, url):
        request = self.factory.get(url)
        request.user = self.user
        return request

    def test_access_forbidden_without_company(self):
        self.user.companies.clear()
        with self.assertRaises(PermissionDenied):
            self.view(self.request)

    def test_client_not_belonging_to_user_raise_404(self):
        with self.assertRaises(Http404):
            self.view(self.request, pk=ClientFactory().id)

    def test_create(self):
        url = reverse("clients:create")
        request = self._get_request(url)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        response = self.view(self.request)
        self.assertEqual(response.status_code, 200)
