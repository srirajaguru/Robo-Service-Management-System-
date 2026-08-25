from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import staff_required
from accounts.models import StaffProfile
from ledger.forms import ExpenseForm, PaymentForm
from .forms import ProgressForm, ServiceForm, StatusForm
from .models import Service, ServiceHistory, ServiceProgress
from notification.services.whatsapp import completion_message, inward_message, send_whatsapp_notification


def current_staff(user):
	return getattr(user, "staffprofile", None)


@staff_required
def service_list(request):
	query = request.GET.get("q", "").strip()
	services = Service.objects.select_related("customer", "created_by").order_by("-created_at")
	if query:
		services = services.filter(customer__name__icontains=query) | services.filter(brand__icontains=query) | services.filter(model__icontains=query)
	status = request.GET.get("status")
	if status:
		services = services.filter(status=status)
	return render(request, "services/list.html", {"services": services, "query": query, "status": status})


@staff_required
def service_create(request):
	form = ServiceForm(request.POST or None)
	if request.method == "POST" and form.is_valid():
		service = form.save(commit=False)
		service.created_by = current_staff(request.user)
		service.updated_by = service.created_by
		service.save()
		send_whatsapp_notification(service, "Inward", inward_message(service), service.created_by)
		messages.success(request, f"Service {service} created.")
		return redirect("service_detail", pk=service.pk)
	return render(request, "services/form.html", {"form": form})


@staff_required
def service_detail(request, pk):
	service = get_object_or_404(Service.objects.select_related("customer"), pk=pk)
	return render(request, "services/detail.html", {
		"service": service,
		"status_form": StatusForm(instance=service),
		"progress_form": ProgressForm(),
		"expense_form": ExpenseForm(),
		"payment_form": PaymentForm(),
		"expenses": service.expense_set.order_by("-created_at"),
		"payments": service.payment_set.order_by("-created_at"),
		"progress": service.serviceprogress_set.select_related("created_by"),
		"history": service.servicehistory_set.select_related("changed_by"),
	})


@staff_required
def service_status(request, pk):
	service = get_object_or_404(Service, pk=pk)
	if request.method == "POST":
		form = StatusForm(request.POST, instance=service)
		if form.is_valid() and form.cleaned_data["status"] != service.status:
			old_status = service.status
			service = form.save(commit=False)
			service.updated_by = current_staff(request.user)
			service.save()
			ServiceHistory.objects.create(service=service, old_status=old_status, new_status=service.status, changed_by=current_staff(request.user))
			if service.status == "Completed":
				send_whatsapp_notification(service, "Completed", completion_message(service), current_staff(request.user))
			messages.success(request, "Service status updated.")
	return redirect("service_detail", pk=pk)


@staff_required
def service_progress(request, pk):
	service = get_object_or_404(Service, pk=pk)
	form = ProgressForm(request.POST or None)
	if request.method == "POST" and form.is_valid():
		progress = form.save(commit=False)
		progress.service = service
		progress.created_by = current_staff(request.user)
		progress.save()
		messages.success(request, "Work progress added.")
	return redirect("service_detail", pk=pk)
