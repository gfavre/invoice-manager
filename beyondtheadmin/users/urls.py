from django.urls import path

from beyondtheadmin.users.views import (user_detail_view, user_redirect_view,
                                        user_update_view, CheckoutView, stripe_config, create_checkout_session)


app_name = "users"

urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("checkout/", view=CheckoutView.as_view(), name="checkout"),
    path("config/", stripe_config),
    path("create-checkout-session/", view=create_checkout_session, name="create-checkout-session"),

    path("<str:username>/", view=user_detail_view, name="detail"),
]
