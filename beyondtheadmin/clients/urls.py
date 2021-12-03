from django.urls import path

from .views import (ClientCreateView, ClientDeleteView, ClientListView,
                    ClientUpdateView)


app_name = "clients"
urlpatterns = [
    path("new", view=ClientCreateView.as_view(), name="create"),
    path("<uuid:pk>/edit", view=ClientUpdateView.as_view(), name="update"),
    path("<uuid:pk>/delete", view=ClientDeleteView.as_view(), name="delete"),
    path('', view=ClientListView.as_view(), name="list"),
]
