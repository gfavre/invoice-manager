from django.urls import path

from beyondtheadmin.users.views import (user_detail_view, user_redirect_view,
                                        user_update_view, CheckoutView, stripe_config, create_checkout_session, CreateStripeCheckoutSessionView)

from . import views as user_views
app_name = "users"

urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("config/", stripe_config),
    path("create-checkout-session/", view=CreateStripeCheckoutSessionView.as_view(), name="create-checkout-session"),
    path("checkout/success", view=user_views.CheckoutSuccessView, name="create_checkout_session_success"),
    path("checkout/cancel", view=user_views.CheckoutCancelView, name="create_checkout_session_cancel"),

    path("checkout/", view=CheckoutView.as_view(), name="checkout"),

    path("<str:username>/", view=user_detail_view, name="detail"),
]
