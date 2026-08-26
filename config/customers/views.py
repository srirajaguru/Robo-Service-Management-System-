from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from accounts.decorators import staff_required
from .models import Customer
from .forms import CustomerForm


@staff_required
def customer_list(request):
    query = request.GET.get('q', '').strip()
    customers_qs = Customer.objects.all().order_by('-created_at')

    if query:
        customers_qs = customers_qs.filter(
            Q(name__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(alternate_phone__icontains=query) |
            Q(customer_id__icontains=query) |
            Q(address__icontains=query)
        )

    paginator = Paginator(customers_qs, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'customers/list.html', {
        'customers': page_obj,
        'page_obj': page_obj,
        'query': query,
        'total_customers_count': Customer.objects.count(),
    })


@staff_required
def customer_create(request):
    form = CustomerForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            phone = form.cleaned_data.get('phone_number')
            existing = Customer.objects.filter(phone_number=phone).first()
            if existing and not request.POST.get('confirm_duplicate'):
                messages.warning(
                    request,
                    f"A customer with phone {phone} already exists ({existing.name} - {existing.customer_id}). "
                    f"Check below if this is the same customer or confirm to proceed."
                )
                return render(request, 'customers/form.html', {
                    'form': form,
                    'existing_customer': existing,
                    'title': 'New Customer Registration'
                })

            customer = form.save()
            messages.success(request, f"Customer {customer.name} ({customer.customer_id}) created successfully.")
            next_url = request.GET.get('next')
            if next_url == 'inward':
                return redirect(f"/service/inward/?selected_customer={customer.pk}")
            return redirect('customer_detail', pk=customer.pk)

    return render(request, 'customers/form.html', {
        'form': form,
        'title': 'New Customer Registration',
    })


@staff_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    form = CustomerForm(request.POST or None, instance=customer)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f"Customer {customer.name} details updated.")
        return redirect('customer_detail', pk=customer.pk)

    return render(request, 'customers/form.html', {
        'form': form,
        'customer': customer,
        'title': f'Edit Customer: {customer.name}',
    })


@staff_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    services = customer.services.select_related('created_by').order_by('-created_at')
    
    return render(request, 'customers/detail.html', {
        'customer': customer,
        'services': services,
    })


@staff_required
def customer_search_api(request):
    """AJAX endpoint for searching customers in Service Inward modal/autocomplete."""
    query = request.GET.get('q', '').strip()
    if not query or len(query) < 2:
        return JsonResponse({'results': []})

    results = []
    qs = Customer.objects.filter(
        Q(name__icontains=query) |
        Q(phone_number__icontains=query) |
        Q(alternate_phone__icontains=query) |
        Q(customer_id__icontains=query)
    )[:10]

    for c in qs:
        results.append({
            'id': c.pk,
            'customer_id': c.customer_id,
            'name': c.name,
            'phone': c.phone_number,
            'alternate_phone': c.alternate_phone,
            'email': c.email,
            'address': c.address,
            'total_services': c.total_services,
        })

    return JsonResponse({'results': results})
