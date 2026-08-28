from django.urls import path
from .views import (
    customer_list, customer_create, customer_detail, customer_edit,
    customer_search_api, customer_quick_create_api
)

urlpatterns = [
    path('', customer_list, name='customer_list'),
    path('new/', customer_create, name='customer_create'),
    path('<int:pk>/', customer_detail, name='customer_detail'),
    path('<int:pk>/edit/', customer_edit, name='customer_edit'),
    path('api/search/', customer_search_api, name='customer_search_api'),
    path('api/quick-create/', customer_quick_create_api, name='customer_quick_create_api'),
]
