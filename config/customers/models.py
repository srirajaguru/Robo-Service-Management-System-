from django.db import models
from django.utils import timezone


class Customer(models.Model):
    customer_id = models.CharField(max_length=20, unique=True, editable=False, db_index=True, default='')
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, db_index=True)
    alternate_phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new and not self.customer_id:
            # Generate ID after initial save or compute next sequence
            super().save(*args, **kwargs)
            year = self.created_at.year if self.created_at else timezone.now().year
            self.customer_id = f"CUS-{year}-{self.pk:05d}"
            super().save(update_fields=['customer_id'])
            return
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.customer_id} - {self.phone_number})"

    # Backwards compatibility alias
    @property
    def customer(self):
        return self.customer_id

    @property
    def total_services(self):
        return self.services.count()

    @property
    def pending_services(self):
        return self.services.filter(status='Pending').count()

    @property
    def in_progress_services(self):
        return self.services.filter(status='In Progress').count()

    @property
    def completed_services(self):
        return self.services.filter(status='Completed').count()

    @property
    def delivered_services(self):
        return self.services.filter(status='Delivered').count()

    @property
    def total_billed_amount(self):
        return sum(s.total_amount for s in self.services.all())

    @property
    def total_paid_amount(self):
        return sum(s.total_paid for s in self.services.all())

    @property
    def total_outstanding_amount(self):
        return max(0, self.total_billed_amount - self.total_paid_amount)
