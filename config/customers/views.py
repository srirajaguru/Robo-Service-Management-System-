from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import staff_required
from services.models import Service
from .forms import CustomerForm
from .models import Customer


@staff_required
def customer_list(request):
	query = request.GET.get("q", "").strip()
	customers = Customer.objects.all().order_by("-created_at")
	if query:
		customers = customers.filter(Q(name__icontains=query) | Q(phone_number__icontains=query) | Q(customer__icontains=query))
	return render(request, "customers/list.html", {"customers": customers, "query": query})


@staff_required
def customer_create(request):
	form = CustomerForm(request.POST or None)
	if request.method == "POST" and form.is_valid():
		customer = form.save()
		messages.success(request, f"Customer {customer.customer} created.")
		return redirect("customer_detail", pk=customer.pk)
	return render(request, "customers/form.html", {"form": form})


@staff_required
def customer_detail(request, pk):
	customer = get_object_or_404(Customer, pk=pk)
	services = Service.objects.filter(customer=customer).order_by("-created_at")
	return render(request, "customers/detail.html", {"customer": customer, "services": services})
