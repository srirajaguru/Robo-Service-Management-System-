from django.contrib import admin
from .models import Service, ServiceHistory, ServiceProgress


class ServiceHistoryInline(admin.TabularInline):
    model = ServiceHistory
    extra = 0
    readonly_fields = ['changed_at']


class ServiceProgressInline(admin.TabularInline):
    model = ServiceProgress
    extra = 0
    readonly_fields = ['created_at']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [
        'service_id', 'customer', 'device_type', 'brand', 'model',
        'status', 'priority', 'expected_completion_date', 'created_by', 'created_at'
    ]
    list_filter = ['status', 'device_type', 'priority', 'created_at']
    search_fields = ['service_id', 'customer__name', 'customer__phone_number', 'brand', 'model', 'serial_number']
    readonly_fields = ['service_id', 'created_at', 'updated_at', 'completed_at', 'delivered_at']
    inlines = [ServiceProgressInline, ServiceHistoryInline]


@admin.register(ServiceHistory)
class ServiceHistoryAdmin(admin.ModelAdmin):
    list_display = ['service', 'old_status', 'new_status', 'changed_by', 'changed_at']
    list_filter = ['old_status', 'new_status', 'changed_at']
    search_fields = ['service__service_id']


@admin.register(ServiceProgress)
class ServiceProgressAdmin(admin.ModelAdmin):
    list_display = ['service', 'progress_description', 'created_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['service__service_id', 'progress_description']
