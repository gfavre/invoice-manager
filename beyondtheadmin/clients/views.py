from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import ClientForm
from .models import Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('clients:list')
    template_name = 'clients/create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        self.object.users.add(self.request.user)
        return HttpResponseRedirect(self.get_success_url())


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('clients:list')
    template_name = 'clients/confirm_delete.html'

    def get_queryset(self):
        return Client.objects.filter(users=self.request.user)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'clients/list.html'

    def get_queryset(self):
        return Client.objects.filter(users=self.request.user)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('clients:list')
    template_name = 'clients/update.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return Client.objects.filter(users=self.request.user)
