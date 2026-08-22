from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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


@login_required
def admin_dashboard(request):

    if not request.user.is_superuser:
        return redirect("staff_dashboard")

    return render(request, "accounts/admin_dashboard.html")


@login_required
def staff_dashboard(request):

    if request.user.is_superuser:
        return redirect("admin_dashboard")

    if not hasattr(request.user, "staffprofile"):
        logout(request)
        return redirect("login")

    return render(request, "accounts/staff_dashboard.html")


def logout_view(request):

    logout(request)

    return redirect("login")