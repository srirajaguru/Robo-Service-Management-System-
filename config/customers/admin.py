from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_id', 'name', 'phone_number', 'alternate_phone', 'email', 'created_at']
    search_fields = ['customer_id', 'name', 'phone_number', 'email', 'address']
    list_filter = ['created_at']
    readonly_fields = ['customer_id', 'created_at', 'updated_at']
