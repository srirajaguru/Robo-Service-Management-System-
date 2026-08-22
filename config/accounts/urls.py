from django.urls import path
from .views import login_view, admin_dashboard, staff_dashboard, logout_view

urlpatterns = [
    path("login/", login_view, name="login"),
    path(
        "admin/",
        admin_dashboard,
        name="admin_dashboard"
    ),

    path(
        "dashboard/",
        staff_dashboard,
        name="staff_dashboard"
    ),

    path(
        "logout/",
        logout_view,
        name="logout"
    ),
]