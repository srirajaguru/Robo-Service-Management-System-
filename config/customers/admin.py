from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	list_display = ("customer", "name", "phone_number", "email", "created_at")
	search_fields = ("customer", "name", "phone_number", "email")
	readonly_fields = ("customer", "created_at", "updated_at")
