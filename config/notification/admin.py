from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['notification_type', 'phone_number', 'service', 'customer', 'status', 'sent_at', 'sent_by']
    list_filter = ['notification_type', 'status', 'sent_at']
    search_fields = ['phone_number', 'message', 'customer__name']
    readonly_fields = ['sent_at']
