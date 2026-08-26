from django.contrib import admin
from .models import Expense, Payment, LedgerEntry, Invoice


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['service', 'expense_type', 'description', 'amount', 'created_by', 'created_at']
    list_filter = ['expense_type', 'created_at']
    search_fields = ['service__service_id', 'description']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['service', 'amount', 'payment_method', 'reference_number', 'payment_date', 'received_by']
    list_filter = ['payment_method', 'payment_date']
    search_fields = ['service__service_id', 'reference_number']


@admin.register(LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = ['service', 'action', 'description', 'amount', 'created_by', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['service__service_id', 'description']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'service', 'invoice_date', 'total_amount', 'paid_amount', 'balance_amount', 'created_by']
    list_filter = ['invoice_date']
    search_fields = ['invoice_number', 'service__service_id', 'service__customer__name']
    readonly_fields = ['invoice_number', 'created_at']
