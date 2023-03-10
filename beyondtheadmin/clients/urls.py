from django.urls import path

from .views.dashboard import ClientAppView, ClientDeleteView, ClientListView


app_name = "clients"
urlpatterns = [
    path("new", view=ClientAppView.as_view(), name="create"),
    path("<uuid:pk>/edit", view=ClientAppView.as_view(), name="update"),
    path("<uuid:pk>/delete", view=ClientDeleteView.as_view(), name="delete"),
    path("", view=ClientListView.as_view(), name="list"),
]
