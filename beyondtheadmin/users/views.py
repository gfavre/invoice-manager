from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.http.response import JsonResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, RedirectView, TemplateView, UpdateView

from rest_framework import permissions
from rest_framework.views import APIView

import stripe

from .serializers import ProductSerializer
from .products import PRODUCTS


User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Infos successfully updated")
        )
        return super().form_valid(form)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()



class StripeAPIView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        conf = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(conf, safe=False)




class CreateStripeCheckoutSessionView(StripeAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = PRODUCTS[serializer.validated_data['code']]
        try:
            breakpoint()
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                success_url=request.build_absolute_uri(reverse('users:create_checkout_session_success')),
                cancel_url=request.build_absolute_uri(reverse('users:create_checkout_session_cancel')),
                customer_email=request.user.email,
                client_reference_id=request.user.id,
                line_items=[
                    {
                        'name': 'Mesfactures',
                        'description': product.description,
                        'amount': product.price,
                        'currency': 'CHF',
                        'quantity': 1,
                    },
                ],
            )
        except Exception as e:
            return JsonResponse({'error': str(e)})
        return JsonResponse({'sessionId': checkout_session['id']})



class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = "users/checkout.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PricesAPIView(StripeAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        prices = stripe.Price.list()
        return JsonResponse(prices)


class CheckoutSuccessView(LoginRequiredMixin, TemplateView):
    template_name = "users/checkout_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CheckoutCancelView(LoginRequiredMixin, TemplateView):
    template_name = "users/checkout_cancel.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
