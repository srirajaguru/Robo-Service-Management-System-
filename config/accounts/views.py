from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone

from customers.models import Customer
from services.models import Service
from ledger.models import Expense, Payment, LedgerEntry
from notification.models import Notification
from .models import StaffProfile
from .forms import LoginForm, StaffCreationForm, StaffEditForm
from .decorators import admin_required, staff_required


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or (hasattr(request.user, 'staffprofile') and request.user.staffprofile.role == 'Admin'):
            return redirect('admin_dashboard')
        return redirect('staff_dashboard')

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.is_active:
                messages.error(request, "This account is inactive. Please contact the administrator.")
                return render(request, 'accounts/login.html', {'form': form})

            # Check staff profile status if not superuser
            if not user.is_superuser:
                profile = getattr(user, 'staffprofile', None)
                if not profile:
                    messages.error(request, "No staff profile associated with this user. Contact Admin.")
                    return render(request, 'accounts/login.html', {'form': form})
                if not profile.is_active:
                    messages.error(request, "Your staff account has been deactivated. Contact Admin.")
                    return render(request, 'accounts/login.html', {'form': form})

            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")

            if user.is_superuser or (hasattr(user, 'staffprofile') and user.staffprofile.role == 'Admin'):
                return redirect('admin_dashboard')
            return redirect('staff_dashboard')
        else:
            messages.error(request, "Invalid username or password. Please check your credentials.")

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been successfully logged out.")
    return redirect('login')


def get_dashboard_context(user):
    all_services = Service.objects.select_related('customer', 'created_by').all()
    
    total_customers = Customer.objects.count()
    total_services = all_services.count()
    pending_services = all_services.filter(status='Pending').count()
    in_progress_services = all_services.filter(status='In Progress').count()
    completed_services = all_services.filter(status='Completed').count()
    delivered_services = all_services.filter(status='Delivered').count()
    cancelled_services = all_services.filter(status='Cancelled').count()

    overdue_qs = all_services.filter(
        expected_completion_date__lt=timezone.localdate(),
        status__in=['Pending', 'In Progress']
    ).order_by('expected_completion_date')
    overdue_count = overdue_qs.count()

    # Device statistics
    laptop_count = all_services.filter(device_type__iexact='Laptop').count()
    desktop_count = all_services.filter(device_type__iexact='Desktop').count()
    printer_count = all_services.filter(device_type__iexact='Printer').count()
    cctv_count = all_services.filter(device_type__iexact='CCTV').count()
    ups_count = all_services.filter(device_type__iexact='UPS').count()
    other_count = total_services - (laptop_count + desktop_count + printer_count + cctv_count + ups_count)

    # Financial KPIs
    total_revenue = sum((s.total_amount for s in all_services), Decimal('0.00'))
    total_expenses = Expense.objects.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    total_collected = Payment.objects.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    outstanding_amount = max(Decimal('0.00'), total_revenue - total_collected)
    net_margin = total_revenue - total_expenses

    recent_services = all_services.order_by('-created_at')[:8]
    recent_notifications = Notification.objects.select_related('service', 'customer').order_by('-sent_at')[:6]

    return {
        'total_customers': total_customers,
        'total_services': total_services,
        'pending_services': pending_services,
        'in_progress_services': in_progress_services,
        'completed_services': completed_services,
        'delivered_services': delivered_services,
        'cancelled_services': cancelled_services,
        'overdue_services': overdue_count,
        'overdue_list': overdue_qs[:5],
        'laptop_services': laptop_count,
        'desktop_services': desktop_count,
        'printer_services': printer_count,
        'cctv_services': cctv_count,
        'ups_services': ups_count,
        'other_services': max(0, other_count),
        'total_revenue': total_revenue,
        'total_expenses': total_expenses,
        'total_collected': total_collected,
        'total_amount': total_revenue,
        'paid_amount': total_collected,
        'outstanding_amount': outstanding_amount,
        'net_margin': net_margin,
        'recent_services': recent_services,
        'services': recent_services,
        'recent_notifications': recent_notifications,
        'notification_count': Notification.objects.count(),
        'total_staff_count': StaffProfile.objects.count(),
    }


@admin_required
def admin_dashboard(request):
    ctx = get_dashboard_context(request.user)
    ctx['is_admin_view'] = True
    return render(request, 'accounts/admin_dashboard.html', ctx)


@staff_required
def staff_dashboard(request):
    if request.user.is_superuser or (hasattr(request.user, 'staffprofile') and request.user.staffprofile.role == 'Admin'):
        return redirect('admin_dashboard')
    ctx = get_dashboard_context(request.user)
    ctx['is_admin_view'] = False
    return render(request, 'accounts/staff_dashboard.html', ctx)


@staff_required
def dashboard_dispatch(request):
    if request.user.is_superuser or (hasattr(request.user, 'staffprofile') and request.user.staffprofile.role == 'Admin'):
        return redirect('admin_dashboard')
    return redirect('staff_dashboard')


# Admin Staff Management Views
@admin_required
def staff_list(request):
    staff_profiles = StaffProfile.objects.select_related('user').all().order_by('name')
    return render(request, 'accounts/staff_list.html', {'staff_list': staff_profiles})


@admin_required
def staff_create(request):
    form = StaffCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        profile = form.save()
        messages.success(request, f"Staff account for {profile.name} created successfully.")
        return redirect('staff_list')
    return render(request, 'accounts/staff_form.html', {'form': form, 'title': 'Add New Staff Member'})


@admin_required
def staff_edit(request, pk):
    profile = get_object_or_404(StaffProfile, pk=pk)
    form = StaffEditForm(request.POST or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f"Staff account for {profile.name} updated.")
        return redirect('staff_list')
    return render(request, 'accounts/staff_form.html', {'form': form, 'profile': profile, 'title': f'Edit Staff: {profile.name}'})


@admin_required
def staff_toggle_status(request, pk):
    profile = get_object_or_404(StaffProfile, pk=pk)
    if profile.user == request.user:
        messages.warning(request, "You cannot deactivate your own account.")
        return redirect('staff_list')
    profile.is_active = not profile.is_active
    profile.user.is_active = profile.is_active
    profile.user.save()
    profile.save()
    status_str = "activated" if profile.is_active else "deactivated"
    messages.info(request, f"Staff member {profile.name} has been {status_str}.")
    return redirect('staff_list')