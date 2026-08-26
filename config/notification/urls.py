from django.urls import path
from .views import notification_list, notification_resend

urlpatterns = [
    path('', notification_list, name='notification_list'),
    path('<int:pk>/resend/', notification_resend, name='notification_resend'),
]
