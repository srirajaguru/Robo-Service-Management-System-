from django.contrib import admin
from django.urls import include, path
from .views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("accounts/", include("accounts.urls")),
    path("service/", include("accounts.urls")),
    path("service/customers/", include("customers.urls")),
    path("service/", include("services.urls")),
    path("service/ledger/", include("ledger.urls")),
]