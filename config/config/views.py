from django.shortcuts import render
from services.models import Service
from customers.models import Customer


def home(request):
    total_services_completed = Service.objects.filter(status__in=['Completed', 'Delivered']).count() + 1250
    total_customers_served = Customer.objects.count() + 850
    
    return render(request, 'home.html', {
        'total_services_completed': total_services_completed,
        'total_customers_served': total_customers_served,
    })