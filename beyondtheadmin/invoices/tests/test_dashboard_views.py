from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from beyondtheadmin.clients.tests.factories import ClientFactory
from beyondtheadmin.companies.tests.factories import CompanyFactory
from beyondtheadmin.users.tests.factories import UserFactory

from ..views.dashboard import InvoiceCreateView, InvoiceUpdateView
from .factories import InvoiceFactory


class InvoiceCreateViewTests(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = UserFactory()
        self.company = CompanyFactory()
        self.client = ClientFactory(company=self.company)
        self.user.companies.add(self.company)
        self.url = reverse("invoices:create")
        self.request = self._get_request(self.url)
        self.request.user = self.user
        self.view = InvoiceCreateView.as_view()

    def _get_request(self, url):
        request = self.factory.get(url)
        request.user = self.user
        return request

    def test_access_forbidden_without_company(self):
        self.user.companies.clear()
        with self.assertRaises(PermissionDenied):
            self.view(self.request)

    def test_company_query_param_adds_context(self):
        request = self._get_request(self.url + f"?company={self.company.id}")
        response = self.view(request)
        self.assertIn("company", response.context_data)
        self.assertEqual(response.context_data["company"], self.company.id)

    def test_company_query_param_raises_permission_denied(self):
        company = CompanyFactory()
        request = self._get_request(self.url + f"?company={company.id}")
        with self.assertRaises(PermissionDenied):
            self.view(request)

    def test_client_query_param_adds_context(self):
        request = self._get_request(self.url + f"?client={self.client.id}")
        response = self.view(request)
        self.assertIn("client", response.context_data)
        self.assertEqual(response.context_data["client"], self.client.id)

    def test_client_query_param_raises_permission_denied(self):
        client = ClientFactory()
        request = self._get_request(self.url + f"?client={client.id}")
        with self.assertRaises(PermissionDenied):
            self.view(request)


class InvoiceUpdateViewTests(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = UserFactory()
        self.company = CompanyFactory()
        self.client = ClientFactory(company=self.company)
        self.invoice = InvoiceFactory(company=self.company, client=self.client)
        self.user.companies.add(self.company)
        self.url = reverse("invoices:update", kwargs={"pk": self.invoice.id})
        self.request = self._get_request(self.url)
        self.request.user = self.user
        self.view = InvoiceUpdateView.as_view()

    def _get_request(self, url):
        request = self.factory.get(url)
        request.user = self.user
        return request

    def raise_404_if_not_draft(self):
        self.invoice.set_sent()
        with self.assertRaises(Http404):
            self.view(self.request, pk=self.invoice.id)

    def test_access_forbidden_without_company(self):
        self.user.companies.clear()
        with self.assertRaises(PermissionDenied):
            self.view(self.request, pk=self.invoice.id)

    def test_access_forbidden(self):
        self.invoice.company = CompanyFactory()
        self.invoice.created_by = UserFactory()
        self.invoice.save()
        with self.assertRaises(PermissionDenied):
            self.view(self.request, pk=self.invoice.id)

    def test_invoice_in_context(self):
        response = self.view(self.request, pk=self.invoice.id)
        self.assertEqual(response.status_code, 200)
        self.assertIn("invoice", response.context_data)
        self.assertEqual(response.context_data["invoice"], self.invoice)
