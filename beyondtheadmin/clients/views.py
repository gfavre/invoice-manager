from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import ClientForm
from .models import Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/create.html'
    success_url = reverse_lazy('clients:list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'clients/confirm_delete.html'
    success_url = reverse_lazy('clients:list')


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'clients/list.html'


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/update.html'
    success_url = reverse_lazy('clients:list')
