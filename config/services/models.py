from decimal import Decimal
from django.db import models
from django.utils import timezone
from customers.models import Customer


class Service(models.Model):
    DEVICE_TYPES = [
        ('Laptop', 'Laptop'),
        ('Desktop', 'Desktop Computer / PC'),
        ('Printer', 'Printer / Scanner'),
        ('CCTV', 'CCTV Camera / DVR'),
        ('UPS', 'UPS / Power Inverter'),
        ('Xerox', 'Xerox / Copier Machine'),
        ('Projector', 'Projector'),
        ('Other', 'Other Technical Device'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low Priority'),
        ('Medium', 'Medium Priority'),
        ('High', 'High Priority'),
        ('Urgent', 'Urgent / Express Service'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending (Received)'),
        ('In Progress', 'In Progress (Diagnosis/Work)'),
        ('Completed', 'Completed (Ready for Delivery)'),
        ('Delivered', 'Delivered (Collected by Customer)'),
        ('Cancelled', 'Cancelled'),
    ]

    service_id = models.CharField(max_length=20, unique=True, editable=False, db_index=True, default='')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='services')
    
    # Device details
    device_type = models.CharField(max_length=50, choices=DEVICE_TYPES, default='Laptop')
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, blank=True, default='')
    asset_number = models.CharField(max_length=100, blank=True, default='')
    physical_condition = models.TextField(blank=True, default='', help_text="e.g. Scratches on lid, minor dent, good condition")
    accessories = models.TextField(blank=True, default='', help_text="e.g. Charger, Power Cable, Bag, Mouse")

    # Complaint & Diagnosis
    complaint = models.TextField(help_text="Customer's reported problem")
    initial_diagnosis = models.TextField(blank=True, default='', help_text="Initial technical findings")
    technician_notes = models.TextField(blank=True, default='', help_text="Internal notes")

    # Service meta
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES, default='Medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    expected_completion_date = models.DateField(blank=True, null=True)

    # Financials (all optional with default 0.00)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), blank=True)
    service_charge = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), blank=True)

    # Staff attribution
    created_by = models.ForeignKey(
        'accounts.StaffProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_services'
    )
    updated_by = models.ForeignKey(
        'accounts.StaffProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_services'
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def save(self, *args, **kwargs):
        if self.service_charge is None:
            self.service_charge = Decimal('0.00')
        if self.estimated_cost is None:
            self.estimated_cost = Decimal('0.00')
        if self.discount is None:
            self.discount = Decimal('0.00')

        is_new = self.pk is None
        if is_new and not self.service_id:
            super().save(*args, **kwargs)
            year = self.created_at.year if self.created_at else timezone.now().year
            self.service_id = f"SRV-{year}-{self.pk:05d}"
            super().save(update_fields=['service_id'])
            return
        super().save(*args, **kwargs)

    def __str__(self):
        return self.service_id if self.service_id else f"SRV-ID-{self.pk}"

    @property
    def total_expenses(self):
        """Sum of all spare parts and additional items from ledger.Expense."""
        total = sum(exp.amount for exp in self.expenses.all())
        return total or Decimal('0.00')

    @property
    def subtotal_amount(self):
        """Service charge + spare parts."""
        charge = self.service_charge if self.service_charge is not None else Decimal('0.00')
        return charge + self.total_expenses

    @property
    def total_amount(self):
        """Subtotal minus discount."""
        disc = self.discount if self.discount is not None else Decimal('0.00')
        total = self.subtotal_amount - disc
        return total if total > Decimal('0.00') else Decimal('0.00')

    @property
    def total_paid(self):
        """Sum of all settled payments from ledger.Payment."""
        total = sum(p.amount for p in self.payments.all())
        return total or Decimal('0.00')

    @property
    def balance_amount(self):
        """Remaining balance due."""
        bal = self.total_amount - self.total_paid
        return bal if bal > Decimal('0.00') else Decimal('0.00')

    @property
    def payment_status(self):
        """Returns Unpaid, Partially Paid, or Paid based on total_paid and balance_amount."""
        if self.total_paid <= Decimal('0.00'):
            return "Unpaid"
        elif self.balance_amount <= Decimal('0.00'):
            return "Paid"
        else:
            return "Partially Paid"

    @property
    def is_overdue(self):
        """Check if expected completion date has passed while still incomplete."""
        if self.expected_completion_date and self.status in ['Pending', 'In Progress']:
            return timezone.now().date() > self.expected_completion_date
        return False


class ServiceHistory(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='history')
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey('accounts.StaffProfile', on_delete=models.SET_NULL, null=True, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['-changed_at']
        verbose_name_plural = 'Service Histories'


class ServiceProgress(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='progress')
    progress_description = models.TextField(help_text="Detailed technical progress update")
    created_by = models.ForeignKey('accounts.StaffProfile', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Service Progress Updates'
