from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Sum
from django.core.paginator import Paginator
from django.http import JsonResponse
from accounts.decorators import staff_required
from customers.models import Customer
from ledger.models import Expense, Payment, LedgerEntry, Invoice
from ledger.forms import ExpenseForm, PaymentForm
from notification.services.whatsapp import (
    send_whatsapp_notification, inward_message, completion_message,
    generate_whatsapp_web_url
)
from .models import Service, ServiceHistory, ServiceProgress
from .forms import ServiceInwardForm, ServiceEditForm, StatusUpdateForm, ProgressUpdateForm


def get_current_staff(user):
    return getattr(user, 'staffprofile', None)


@staff_required
def service_list(request):
    services_qs = Service.objects.select_related('customer', 'created_by').all().order_by('-created_at')
    
    # Status filter tab
    status_tab = request.GET.get('status', 'all')
    if status_tab == 'overdue':
        services_qs = services_qs.filter(
            expected_completion_date__lt=timezone.localdate(),
            status__in=['Pending', 'In Progress']
        )
    elif status_tab in ['Pending', 'In Progress', 'Completed', 'Delivered', 'Cancelled']:
        services_qs = services_qs.filter(status=status_tab)

    # Device type filter
    device_filter = request.GET.get('device')
    if device_filter:
        services_qs = services_qs.filter(device_type=device_filter)

    # Priority filter
    priority_filter = request.GET.get('priority')
    if priority_filter:
        services_qs = services_qs.filter(priority=priority_filter)

    # Search query
    query = request.GET.get('q', '').strip()
    if query:
        services_qs = services_qs.filter(
            Q(service_id__icontains=query) |
            Q(customer__name__icontains=query) |
            Q(customer__phone_number__icontains=query) |
            Q(brand__icontains=query) |
            Q(model__icontains=query) |
            Q(serial_number__icontains=query) |
            Q(complaint__icontains=query)
        )

    paginator = Paginator(services_qs, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Counts for quick tabs
    all_count = Service.objects.count()
    pending_count = Service.objects.filter(status='Pending').count()
    in_progress_count = Service.objects.filter(status='In Progress').count()
    completed_count = Service.objects.filter(status='Completed').count()
    delivered_count = Service.objects.filter(status='Delivered').count()
    overdue_count = Service.objects.filter(
        expected_completion_date__lt=timezone.localdate(),
        status__in=['Pending', 'In Progress']
    ).count()

    return render(request, 'services/list.html', {
        'services': page_obj,
        'page_obj': page_obj,
        'status_tab': status_tab,
        'device_filter': device_filter,
        'priority_filter': priority_filter,
        'query': query,
        'all_count': all_count,
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count,
        'delivered_count': delivered_count,
        'overdue_count': overdue_count,
        'device_choices': Service.DEVICE_TYPES,
        'priority_choices': Service.PRIORITY_CHOICES,
    })


@staff_required
def service_inward(request):
    staff = get_current_staff(request.user)
    selected_customer_id = request.GET.get('selected_customer')
    selected_customer = None

    if selected_customer_id:
        selected_customer = Customer.objects.filter(pk=selected_customer_id).first()

    initial_data = {}
    if selected_customer:
        initial_data['customer'] = selected_customer

    form = ServiceInwardForm(request.POST or None, initial=initial_data)

    if request.method == 'POST':
        if form.is_valid():
            service = form.save(commit=False)
            service.accessories = form.cleaned_data.get('accessories', '')
            service.discount = Decimal('0.00')
            service.service_charge = service.service_charge or Decimal('0.00')
            service.estimated_cost = service.estimated_cost or Decimal('0.00')
            service.created_by = staff
            service.updated_by = staff
            service.save()

            # Record initial Ledger Entry
            ledger_amount = service.service_charge if service.service_charge > Decimal('0.00') else service.estimated_cost
            LedgerEntry.objects.create(
                service=service,
                action='Inward Created',
                description=f"Device inward received: {service.device_type} ({service.brand} {service.model}) - Complaint: {service.complaint[:100]}",
                amount=ledger_amount,
                created_by=staff
            )

            # Record initial Service History
            ServiceHistory.objects.create(
                service=service,
                old_status='None',
                new_status='Pending',
                changed_by=staff,
                remarks='Initial device receipt at service center.'
            )

            # Trigger Inward WhatsApp Notification
            if request.POST.get('send_whatsapp') != '0':
                msg = inward_message(service)
                send_whatsapp_notification(service, 'Inward', msg, staff)

            messages.success(request, f"Service Inward created successfully! Service ID: {service.service_id}")
            return redirect('service_detail', pk=service.pk)

    recent_customers = Customer.objects.all().order_by('-created_at')[:15]

    return render(request, 'services/inward_form.html', {
        'form': form,
        'selected_customer': selected_customer,
        'recent_customers': recent_customers,
    })


@staff_required
def service_detail(request, pk):
    service = get_object_or_404(
        Service.objects.select_related('customer', 'created_by', 'updated_by'),
        pk=pk
    )

    expenses = service.expenses.select_related('created_by').order_by('-created_at')
    payments = service.payments.select_related('received_by').order_by('-created_at')
    progress_updates = service.progress.select_related('created_by').order_by('-created_at')
    status_history = service.history.select_related('changed_by').order_by('-changed_at')
    ledger_entries = service.ledger_entries.select_related('created_by').order_by('-created_at')

    status_form = StatusUpdateForm(initial={'status': service.status})
    progress_form = ProgressUpdateForm()
    expense_form = ExpenseForm()
    payment_form = PaymentForm()

    # Generate one-click WhatsApp web links
    inward_msg_text = inward_message(service)
    completion_msg_text = completion_message(service)
    customer_phone = service.customer.phone_number if service.customer else ''
    whatsapp_inward_url = generate_whatsapp_web_url(customer_phone, inward_msg_text)
    whatsapp_completion_url = generate_whatsapp_web_url(customer_phone, completion_msg_text)

    return render(request, 'services/detail.html', {
        'service': service,
        'customer': service.customer,
        'expenses': expenses,
        'payments': payments,
        'progress_updates': progress_updates,
        'status_history': status_history,
        'ledger_entries': ledger_entries,
        'status_form': status_form,
        'progress_form': progress_form,
        'expense_form': expense_form,
        'payment_form': payment_form,
        'whatsapp_inward_url': whatsapp_inward_url,
        'whatsapp_completion_url': whatsapp_completion_url,
    })


@staff_required
def service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    form = ServiceEditForm(request.POST or None, instance=service)

    if request.method == 'POST' and form.is_valid():
        svc = form.save(commit=False)
        svc.updated_by = get_current_staff(request.user)
        svc.save()
        messages.success(request, f"Service {service.service_id} details updated.")
        return redirect('service_detail', pk=service.pk)

    return render(request, 'services/edit_form.html', {
        'form': form,
        'service': service,
    })


@staff_required
def service_status_update(request, pk):
    service = get_object_or_404(Service, pk=pk)
    staff = get_current_staff(request.user)

    if request.method == 'POST':
        form = StatusUpdateForm(request.POST)
        if form.is_valid():
            new_status = form.cleaned_data['status']
            remarks = form.cleaned_data.get('remarks', '').strip()

            if new_status != service.status:
                old_status = service.status
                service.status = new_status
                service.updated_by = staff

                # Handle specific completion / delivery timestamps
                if new_status == 'Completed':
                    service.completed_at = timezone.now()
                    # Trigger Completion WhatsApp notification
                    if request.POST.get('send_whatsapp') == '1':
                        msg = completion_message(service)
                        send_whatsapp_notification(service, 'Completed', msg, staff)

                elif new_status == 'Delivered':
                    service.delivered_at = timezone.now()

                service.save()

                # Record status history
                ServiceHistory.objects.create(
                    service=service,
                    old_status=old_status,
                    new_status=new_status,
                    changed_by=staff,
                    remarks=remarks or f"Status changed from {old_status} to {new_status}"
                )

                # Record in ledger
                LedgerEntry.objects.create(
                    service=service,
                    action='Status Change',
                    description=f"Status updated: {old_status} ➔ {new_status}" + (f" ({remarks})" if remarks else ""),
                    created_by=staff
                )

                messages.success(request, f"Service status changed to {new_status}.")
            else:
                messages.info(request, f"Status is already {new_status}.")

    return redirect('service_detail', pk=service.pk)


@staff_required
def service_progress_add(request, pk):
    service = get_object_or_404(Service, pk=pk)
    staff = get_current_staff(request.user)

    if request.method == 'POST':
        form = ProgressUpdateForm(request.POST)
        if form.is_valid():
            progress = form.save(commit=False)
            progress.service = service
            progress.created_by = staff
            progress.save()

            # Record in ledger
            LedgerEntry.objects.create(
                service=service,
                action='Work Progress',
                description=f"Work update: {progress.progress_description[:120]}",
                created_by=staff
            )

            service.updated_by = staff
            service.save(update_fields=['updated_by', 'updated_at'])
            messages.success(request, "Technical work progress recorded.")

    return redirect('service_detail', pk=service.pk)


def service_track_public(request):
    """
    Public Service Tracking lookup for customers.
    Does not require login. Allows tracking by Service ID or Phone Number.
    """
    query = request.GET.get('q', '').strip()
    service_result = None
    results_list = []
    error_msg = None

    if query:
        # Check by exact or partial service ID
        exact_service = Service.objects.filter(service_id__iexact=query).select_related('customer').first()
        if exact_service:
            service_result = exact_service
        else:
            # Check by phone number
            results_list = Service.objects.filter(
                customer__phone_number__icontains=query
            ).select_related('customer').order_by('-created_at')[:10]
            
            if not results_list:
                error_msg = f"No active service record found for '{query}'. Please check your Service ID or registered phone number."

    return render(request, 'services/track.html', {
        'query': query,
        'service': service_result,
        'results_list': results_list,
        'error_msg': error_msg,
    })
