from django.urls import path
from .views import (
    login_view, logout_view, admin_dashboard, staff_dashboard, dashboard_dispatch,
    staff_list, staff_create, staff_edit, staff_toggle_status
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_dispatch, name='dashboard'),
    path('dashboard/admin/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/staff/', staff_dashboard, name='staff_dashboard'),
    path('staff/', staff_list, name='staff_list'),
    path('staff/new/', staff_create, name='staff_create'),
    path('staff/<int:pk>/edit/', staff_edit, name='staff_edit'),
    path('staff/<int:pk>/toggle/', staff_toggle_status, name='staff_toggle_status'),
]