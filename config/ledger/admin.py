from django.contrib import admin
from .models import Expense, Invoice, LedgerEntry, Payment

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
	list_display = ("service", "description", "amount", "created_by", "created_at")
	list_filter = ("created_at",)
	search_fields = ("service__customer__name", "description")
	readonly_fields = ("created_at",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
	list_display = ("service", "amount", "payment_method", "received_by", "payment_date")
	list_filter = ("payment_method", "payment_date")
	search_fields = ("service__customer__name", "reference_number")
	readonly_fields = ("payment_date", "created_at")


@admin.register(LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):
	list_display = ("service", "action", "amount", "created_by", "created_at")
	list_filter = ("action", "created_at")
	search_fields = ("service__customer__name", "description")
	readonly_fields = ("created_at",)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
	list_display = ("invoice_number", "service", "total_amount", "paid_amount", "balance_amount", "invoice_date")
	search_fields = ("invoice_number", "service__customer__name")
	readonly_fields = ("invoice_date", "created_at")
