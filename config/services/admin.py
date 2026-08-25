from django.contrib import admin
from .models import Service, ServiceHistory, ServiceProgress

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
	list_display = ("service", "customer", "device_type", "status", "price", "created_by", "created_at")
	list_filter = ("status", "device_type", "priority", "created_at")
	search_fields = ("customer__name", "customer__phone_number", "brand", "model", "complaint")
	readonly_fields = ("created_at", "updated_at")


@admin.register(ServiceHistory)
class ServiceHistoryAdmin(admin.ModelAdmin):
	list_display = ("service", "old_status", "new_status", "changed_by", "changed_at")
	list_filter = ("old_status", "new_status", "changed_at")
	readonly_fields = ("changed_at",)


@admin.register(ServiceProgress)
class ServiceProgressAdmin(admin.ModelAdmin):
	list_display = ("service", "created_by", "created_at")
	search_fields = ("service__customer__name", "progress_description")
	readonly_fields = ("created_at",)
