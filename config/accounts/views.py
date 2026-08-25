from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db.models import Sum
from django.utils import timezone

from customers.models import Customer
from services.models import Service
from ledger.models import Payment
from notification.models import Notification
from .decorators import admin_required, staff_required


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            # Admin
            if user.is_superuser:
                return redirect("admin_dashboard")

            # Staff
            if hasattr(user, "staffprofile"):
                return redirect("staff_dashboard")

            # User has no recognized role
            logout(request)
            return render(
                request,
                "accounts/login.html",
                {"error": "You are not authorized to access this system."}
            )

        return render(
            request,
            "accounts/login.html",
            {"error": "Invalid username or password."}
        )

    return render(request, "accounts/login.html")


@admin_required
def admin_dashboard(request):
    return render(request, "accounts/admin_dashboard.html", dashboard_context())


@staff_required
def staff_dashboard(request):
    if request.user.is_superuser:
        return redirect("admin_dashboard")
    return render(request, "accounts/staff_dashboard.html", dashboard_context())


def dashboard_context():
    services = Service.objects.all()
    total_amount = services.aggregate(total=Sum("price"))["total"] or 0
    paid_amount = Payment.objects.aggregate(total=Sum("amount"))["total"] or 0
    recent_services = services.select_related("customer").order_by("-created_at")[:8]
    return {
        "total_customers": Customer.objects.count(),
        "total_services": services.count(),
        "pending_services": services.filter(status="Pending").count(),
        "in_progress_services": services.filter(status="In Progress").count(),
        "completed_services": services.filter(status="Completed").count(),
        "delivered_services": services.filter(status="Delivered").count(),
        "overdue_services": services.filter(
            expected_completion_date__lt=timezone.localdate(),
            status__in=["Pending", "In Progress"],
        ).count(),
        "laptop_services": services.filter(device_type__iexact="Laptop").count(),
        "desktop_services": services.filter(device_type__iexact="Desktop").count(),
        "printer_services": services.filter(device_type__iexact="Printer").count(),
        "other_services": services.exclude(device_type__iexact="Laptop").exclude(device_type__iexact="Desktop").exclude(device_type__iexact="Printer").count(),
        "notification_count": Notification.objects.count(),
        "total_amount": total_amount,
        "paid_amount": paid_amount,
        "outstanding_amount": total_amount - paid_amount,
        "recent_services": recent_services,
        "services": recent_services,
    }


def logout_view(request):

    logout(request)

    return redirect("login")