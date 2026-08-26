from django.urls import path
from .views import (
    service_list, service_inward, service_detail, service_edit,
    service_status_update, service_progress_add, service_track_public
)

urlpatterns = [
    path('inward/', service_inward, name='service_create'),
    path('services/', service_list, name='service_list'),
    path('services/<int:pk>/', service_detail, name='service_detail'),
    path('services/<int:pk>/edit/', service_edit, name='service_edit'),
    path('services/<int:pk>/status/', service_status_update, name='service_status'),
    path('services/<int:pk>/progress/', service_progress_add, name='service_progress'),
    path('track/', service_track_public, name='service_track_public'),
]
