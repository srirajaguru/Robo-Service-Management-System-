from django.contrib import admin
from .models import StaffProfile


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'phone_number', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'is_active']
    search_fields = ['name', 'user__username', 'phone_number']
    readonly_fields = ['created_at']
