from decimal import Decimal
from django.db import models
from django.utils import timezone


class Expense(models.Model):
    EXPENSE_TYPES = [
        ('Spare Part', 'Spare Part (Screen, Keyboard, RAM, SSD, etc.)'),
        ('Motherboard Chip', 'Chip Level / IC / Component'),
        ('Consumable', 'Consumables (Thermal paste, solder, cleaner)'),
        ('Third-Party', 'Third-Party / Specialist Service'),
        ('Transport', 'Courier / Transport Expense'),
        ('Other', 'Other Service Expense'),
    ]

    service = models.ForeignKey('services.Service', on_delete=models.CASCADE, related_name='expenses')
    expense_type = models.CharField(max_length=50, choices=EXPENSE_TYPES, default='Spare Part')
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey('accounts.StaffProfile', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Service Expense'
        verbose_name_plural = 'Service Expenses'

    def __str__(self):
        return f"{self.service.service_id} - {self.description}: ₹{self.amount}"


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('Cash', 'Cash'),
        ('UPI', 'UPI (GPay / PhonePe / Paytm)'),
        ('Card', 'Debit / Credit Card'),
        ('Bank Transfer', 'Net Banking / NEFT'),
        ('Other', 'Other Method'),
    ]

    service = models.ForeignKey('services.Service', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS, default='Cash')
    reference_number = models.CharField(max_length=100, blank=True, default='', help_text="UPI Ref / Transaction ID / Receipt No")
    payment_date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, default='')
    received_by = models.ForeignKey('accounts.StaffProfile', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Service Payment'
        verbose_name_plural = 'Service Payments'

    def __str__(self):
        return f"{self.service.service_id} Payment: ₹{self.amount} via {self.payment_method}"


class LedgerEntry(models.Model):
    ACTION_CHOICES = [
        ('Inward Created', 'Inward Created'),
        ('Status Change', 'Status Change'),
        ('Work Progress', 'Work Progress Update'),
        ('Expense Added', 'Expense / Part Added'),
        ('Payment Received', 'Payment Received'),
        ('Invoice Generated', 'Invoice Generated'),
        ('Delivered', 'Device Delivered'),
        ('Cancelled', 'Service Cancelled'),
        ('Other', 'Other Action'),
    ]

    service = models.ForeignKey('services.Service', on_delete=models.CASCADE, related_name='ledger_entries')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES, default='Other')
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_by = models.ForeignKey('accounts.StaffProfile', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Service Ledger Entry'
        verbose_name_plural = 'Service Ledger Entries'

    def __str__(self):
        return f"{self.service.service_id} [{self.action}]: {self.description}"


class Invoice(models.Model):
    service = models.OneToOneField('services.Service', on_delete=models.CASCADE, related_name='invoice')
    invoice_number = models.CharField(max_length=50, unique=True, editable=False, db_index=True)
    invoice_date = models.DateTimeField(default=timezone.now)
    labor_charge = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    parts_charge = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    other_charges = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    sub_total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    notes = models.TextField(blank=True, default='')
    created_by = models.ForeignKey('accounts.StaffProfile', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new and not self.invoice_number:
            super().save(*args, **kwargs)
            year = self.invoice_date.year if self.invoice_date else timezone.now().year
            self.invoice_number = f"INV-{year}-{self.pk:05d}"
            super().save(update_fields=['invoice_number'])
            return
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.invoice_number} ({self.service.service_id})"
