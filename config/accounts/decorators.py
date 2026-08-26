from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def is_staff_or_admin(user):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    if hasattr(user, 'staffprofile') and user.staffprofile.is_active:
        return True
    return False


def is_admin_user(user):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    if hasattr(user, 'staffprofile') and user.staffprofile.is_active and user.staffprofile.role == 'Admin':
        return True
    return False


def staff_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "Please log in to access the service management system.")
            return redirect('login')
        if not is_staff_or_admin(request.user):
            messages.error(request, "You are not authorized to access this section.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "Please log in with administrator credentials.")
            return redirect('login')
        if not is_admin_user(request.user):
            messages.error(request, "Administrator privileges required for this action.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
