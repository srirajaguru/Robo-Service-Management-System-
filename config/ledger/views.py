import csv
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Q, Count
from django.core.paginator import Paginator
from accounts.decorators import staff_required, admin_required
from services.models import Service
from .models import Expense, Payment, LedgerEntry, Invoice
from .forms import ExpenseForm, PaymentForm, InvoiceForm
from notification.services.whatsapp import send_whatsapp_notification, payment_message


@admin_required
def ledger_list(request):
    entries_qs = LedgerEntry.objects.select_related('service', 'service__customer', 'created_by').all().order_by('-created_at')
    
    action_filter = request.GET.get('action')
    if action_filter:
        entries_qs = entries_qs.filter(action=action_filter)
        
    query = request.GET.get('q', '').strip()
    if query:
        entries_qs = entries_qs.filter(
            Q(service__service_id__icontains=query) |
            Q(service__customer__name__icontains=query) |
            Q(description__icontains=query)
        )

    paginator = Paginator(entries_qs, 30)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Compute high-level financial summary
    all_services = Service.objects.all()
    total_revenue = sum((s.total_amount for s in all_services), Decimal('0.00'))
    total_expenses = Expense.objects.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    total_collected = Payment.objects.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    total_outstanding = max(Decimal('0.00'), total_revenue - total_collected)
    net_margin = total_revenue - total_expenses

    return render(request, 'ledger/list.html', {
        'entries': page_obj,
        'page_obj': page_obj,
        'action_filter': action_filter,
        'query': query,
        'total_revenue': total_revenue,
        'total_expenses': total_expenses,
        'total_collected': total_collected,
        'total_outstanding': total_outstanding,
        'net_margin': net_margin,
        'action_choices': LedgerEntry.ACTION_CHOICES,
    })


@staff_required
def expense_create(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    form = ExpenseForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        expense = form.save(commit=False)
        expense.service = service
        expense.created_by = getattr(request.user, 'staffprofile', None)
        expense.save()

        # Record in ledger
        LedgerEntry.objects.create(
            service=service,
            action='Expense Added',
            description=f"Added {expense.expense_type}: {expense.description}",
            amount=expense.amount,
            created_by=expense.created_by
        )
        messages.success(request, f"Expense of ₹{expense.amount} recorded for {service.service_id}.")

    return redirect('service_detail', pk=service.pk)


@staff_required
def expense_delete(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    service = expense.service
    staff = getattr(request.user, 'staffprofile', None)
    
    LedgerEntry.objects.create(
        service=service,
        action='Other',
        description=f"Removed Expense: {expense.description} (₹{expense.amount})",
        amount=-expense.amount,
        created_by=staff
    )
    expense.delete()
    messages.info(request, "Expense entry deleted and ledger updated.")
    return redirect('service_detail', pk=service.pk)


@staff_required
def payment_create(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    form = PaymentForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        payment = form.save(commit=False)
        payment.service = service
        payment.received_by = getattr(request.user, 'staffprofile', None)
        payment.save()

        # Record in ledger
        ref_text = f" (Ref: {payment.reference_number})" if payment.reference_number else ""
        LedgerEntry.objects.create(
            service=service,
            action='Payment Received',
            description=f"Received ₹{payment.amount} via {payment.payment_method}{ref_text}",
            amount=payment.amount,
            created_by=payment.received_by
        )

        # Notify via WhatsApp
        if request.POST.get('send_whatsapp') == '1':
            send_whatsapp_notification(
                service=service,
                notification_type='Payment',
                message=payment_message(service, payment),
                staff_profile=payment.received_by
            )

        messages.success(request, f"Payment of ₹{payment.amount} recorded. Balance: ₹{service.balance_amount}")

    return redirect('service_detail', pk=service.pk)


@staff_required
def invoice_view(request, service_id):
    service = get_object_or_404(Service.objects.select_related('customer', 'created_by'), pk=service_id)
    
    # Requirement: Only Completed or Delivered services can generate/view official invoices
    if service.status not in ['Completed', 'Delivered']:
        messages.warning(request, "Invoices can only be generated after the service is marked Completed or Delivered.")
        return redirect('service_detail', pk=service.pk)

    # Get or create invoice record
    invoice = getattr(service, 'invoice', None)
    if not invoice:
        labor = service.service_charge if service.service_charge > Decimal('0.00') else service.estimated_cost
        parts = service.total_expenses
        discount = service.discount
        subtotal = labor + parts
        total = max(Decimal('0.00'), subtotal - discount)
        paid = service.total_paid
        balance = max(Decimal('0.00'), total - paid)

        invoice = Invoice.objects.create(
            service=service,
            labor_charge=labor,
            parts_charge=parts,
            other_charges=Decimal('0.00'),
            discount=discount,
            sub_total_amount=subtotal,
            total_amount=total,
            paid_amount=paid,
            balance_amount=balance,
            created_by=getattr(request.user, 'staffprofile', None)
        )
        LedgerEntry.objects.create(
            service=service,
            action='Invoice Generated',
            description=f"Generated Invoice {invoice.invoice_number} (Total: ₹{total})",
            amount=total,
            created_by=invoice.created_by
        )

    return render(request, 'ledger/invoice.html', {
        'service': service,
        'invoice': invoice,
        'customer': service.customer,
        'expenses': service.expenses.all(),
        'payments': service.payments.all(),
        'now': timezone.now(),
    })


@admin_required
def reports_monthly(request):
    current_year = timezone.now().year
    current_month = timezone.now().month

    year = int(request.GET.get('year', current_year))
    month = int(request.GET.get('month', current_month))

    services_qs = Service.objects.filter(
        created_at__year=year,
        created_at__month=month
    ).select_related('customer', 'created_by').order_by('-created_at')

    total_services = services_qs.count()
    completed_count = services_qs.filter(status__in=['Completed', 'Delivered']).count()
    total_billed = sum((s.total_amount for s in services_qs), Decimal('0.00'))
    total_parts = sum((s.total_expenses for s in services_qs), Decimal('0.00'))
    total_collected = sum((s.total_paid for s in services_qs), Decimal('0.00'))
    total_outstanding = sum((s.balance_amount for s in services_qs), Decimal('0.00'))
    net_profit = total_billed - total_parts

    months_list = [
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
        (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
        (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
    ]
    years_list = range(current_year - 3, current_year + 2)

    return render(request, 'reports/monthly.html', {
        'services': services_qs,
        'year': year,
        'month': month,
        'month_name': dict(months_list).get(month, ''),
        'total_services': total_services,
        'completed_count': completed_count,
        'total_billed': total_billed,
        'total_parts': total_parts,
        'total_collected': total_collected,
        'total_outstanding': total_outstanding,
        'net_profit': net_profit,
        'months_list': months_list,
        'years_list': years_list,
    })


@admin_required
def export_monthly_csv(request):
    year = int(request.GET.get('year', timezone.now().year))
    month = int(request.GET.get('month', timezone.now().month))

    services_qs = Service.objects.filter(
        created_at__year=year,
        created_at__month=month
    ).select_related('customer', 'created_by').order_by('created_at')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="ROBO_DIGITAL_Report_{year}_{month:02d}.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Service ID', 'Customer Name', 'Phone', 'Device', 'Brand/Model',
        'Service Date', 'Completion Date', 'Status', 'Staff', 'Labor Charge',
        'Parts Expense', 'Total Billed', 'Total Paid', 'Balance'
    ])

    for s in services_qs:
        writer.writerow([
            s.service_id,
            s.customer.name,
            s.customer.phone_number,
            s.device_type,
            f"{s.brand} {s.model}",
            s.created_at.strftime('%d-%b-%Y'),
            s.completed_at.strftime('%d-%b-%Y') if s.completed_at else '-',
            s.status,
            s.created_by.name if s.created_by else '-',
            f"{s.service_charge:.2f}",
            f"{s.total_expenses:.2f}",
            f"{s.total_amount:.2f}",
            f"{s.total_paid:.2f}",
            f"{s.balance_amount:.2f}",
        ])

    return response


@admin_required
def reports_yearly(request):
    current_year = timezone.now().year
    year = int(request.GET.get('year', current_year))

    monthly_data = []
    total_yearly_services = 0
    total_yearly_revenue = Decimal('0.00')
    total_yearly_expenses = Decimal('0.00')
    total_yearly_collected = Decimal('0.00')

    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for m in range(1, 13):
        m_services = Service.objects.filter(created_at__year=year, created_at__month=m)
        count = m_services.count()
        revenue = sum((s.total_amount for s in m_services), Decimal('0.00'))
        expenses = sum((s.total_expenses for s in m_services), Decimal('0.00'))
        collected = sum((s.total_paid for s in m_services), Decimal('0.00'))
        profit = revenue - expenses

        total_yearly_services += count
        total_yearly_revenue += revenue
        total_yearly_expenses += expenses
        total_yearly_collected += collected

        monthly_data.append({
            'month_num': m,
            'month_name': month_names[m - 1],
            'count': count,
            'revenue': revenue,
            'expenses': expenses,
            'collected': collected,
            'profit': profit,
        })

    years_list = range(current_year - 4, current_year + 2)

    return render(request, 'reports/yearly.html', {
        'year': year,
        'monthly_data': monthly_data,
        'total_yearly_services': total_yearly_services,
        'total_yearly_revenue': total_yearly_revenue,
        'total_yearly_expenses': total_yearly_expenses,
        'total_yearly_collected': total_yearly_collected,
        'total_yearly_profit': total_yearly_revenue - total_yearly_expenses,
        'years_list': years_list,
    })


@admin_required
def export_yearly_csv(request):
    year = int(request.GET.get('year', timezone.now().year))
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="ROBO_DIGITAL_Yearly_Summary_{year}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Month', 'Total Services', 'Revenue (₹)', 'Expenses (₹)', 'Net Margin (₹)', 'Collected (₹)'])

    for m in range(1, 13):
        m_services = Service.objects.filter(created_at__year=year, created_at__month=m)
        count = m_services.count()
        revenue = sum((s.total_amount for s in m_services), Decimal('0.00'))
        expenses = sum((s.total_expenses for s in m_services), Decimal('0.00'))
        collected = sum((s.total_paid for s in m_services), Decimal('0.00'))
        profit = revenue - expenses

        writer.writerow([
            month_names[m - 1],
            count,
            f"{revenue:.2f}",
            f"{expenses:.2f}",
            f"{profit:.2f}",
            f"{collected:.2f}"
        ])

    return response
