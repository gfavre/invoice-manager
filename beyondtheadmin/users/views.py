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


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        conf = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(conf, safe=False)


# Trouver comment faire un descripteur de produit. Je pense que ce devrait être un modèle.
class CreateStripeCheckoutSessionView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        stripe.api_key = settings.STRIPE_SECRET_KEY
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


@csrf_exempt
def create_checkout_session(request):
    breakpoint()
    if request.method == 'POST':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'T-shirt',
                        'quantity': 1,
                        'currency': 'usd',
                        'amount': '2000',
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = "users/checkout.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


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
