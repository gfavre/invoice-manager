from django.urls import path

from .views import CompanyAppView, CompanyDeleteView, CompanyDetailView


app_name = "companies"
urlpatterns = [
    path("new", view=CompanyAppView.as_view(), name="create"),
    path("<uuid:pk>/", view=CompanyDetailView.as_view(), name="detail"),
    path("<uuid:pk>/edit", view=CompanyAppView.as_view(), name="update"),
    path("<uuid:pk>/delete", view=CompanyDeleteView.as_view(), name="delete"),
]
