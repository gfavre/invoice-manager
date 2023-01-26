from django.urls import path

from .views import (
    CompanyCreateView,
    CompanyDeleteView,
    CompanyDetailView,
    CompanyUpdateView,
    CompanyWizardView,
)


app_name = "companies"
urlpatterns = [
    path("wizard", view=CompanyWizardView.as_view(), name="wizard"),
    path("new", view=CompanyCreateView.as_view(), name="create"),
    path("<uuid:pk>/", view=CompanyDetailView.as_view(), name="detail"),
    path("<uuid:pk>/edit", view=CompanyUpdateView.as_view(), name="update"),
    path("<uuid:pk>/delete", view=CompanyDeleteView.as_view(), name="delete"),
]
