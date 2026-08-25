from django.urls import path

from .views import service_create, service_detail, service_list, service_progress, service_status

urlpatterns = [
    path("inward/", service_create, name="service_create"),
    path("services/", service_list, name="service_list"),
    path("services/<int:pk>/", service_detail, name="service_detail"),
    path("services/<int:pk>/status/", service_status, name="service_status"),
    path("services/<int:pk>/progress/", service_progress, name="service_progress"),
]
