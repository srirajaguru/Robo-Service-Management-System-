from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import admin_required, staff_required
from .models import Expense, LedgerEntry, Payment
from .forms import ExpenseForm, PaymentForm
from services.models import Service


@admin_required
def ledger_list(request):
	return render(request, "ledger/list.html", {
		"entries": LedgerEntry.objects.select_related("service", "created_by").order_by("-created_at"),
		"expenses": Expense.objects.select_related("service").order_by("-created_at")[:50],
		"payments": Payment.objects.select_related("service").order_by("-created_at")[:50],
	})


@staff_required
def expense_create(request, service_id):
	service = get_object_or_404(Service, pk=service_id)
	form = ExpenseForm(request.POST or None)
	if request.method == "POST" and form.is_valid():
		expense = form.save(commit=False)
		expense.service = service
		expense.created_by = getattr(request.user, "staffprofile", None)
		expense.save()
		LedgerEntry.objects.create(service=service, action="Expense", description=expense.description, amount=expense.amount, created_by=expense.created_by)
		messages.success(request, "Expense recorded.")
	return redirect("service_detail", pk=service.pk)


@staff_required
def payment_create(request, service_id):
	service = get_object_or_404(Service, pk=service_id)
	form = PaymentForm(request.POST or None)
	if request.method == "POST" and form.is_valid():
		payment = form.save(commit=False)
		payment.service = service
		payment.received_by = getattr(request.user, "staffprofile", None)
		payment.save()
		LedgerEntry.objects.create(service=service, action="Payment", description=f"Payment via {payment.payment_method}", amount=payment.amount, created_by=payment.received_by)
		messages.success(request, "Payment recorded.")
	return redirect("service_detail", pk=service.pk)
