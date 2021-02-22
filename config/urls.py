from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView

from rest_framework.authtoken.views import obtain_auth_token
from beyondtheadmin.dashboard.views import DashboardView
from beyondtheadmin.invoices.views.dashboard import InvoiceDetailView

admin.autodiscover()
admin.site.enable_nav_sidebar = False


urlpatterns = i18n_patterns(
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
      "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),

    path("accounts/", include("allauth.urls")),
    path("companies/", include("beyondtheadmin.companies.urls", namespace="companies")),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("invoices/", include("beyondtheadmin.invoices.urls", namespace="invoices")),
    path("users/", include("beyondtheadmin.users.urls", namespace="users")),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
    # Why is it here? invoices are translated to the client's language. We don't want to find ourselves
    # under a case where one could change the language. Therefore it has to find place here.
    path("invoice/<uuid:pk>/", view=InvoiceDetailView.as_view(), name="invoice-print"),

]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
