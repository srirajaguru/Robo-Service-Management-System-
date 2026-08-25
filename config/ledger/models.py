from django.db import models

class Expense(models.Model):
    service = models.ForeignKey('services.Service', on_delete=models.CASCADE)
    expense_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey('accounts.StaffProfile', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    service = models.ForeignKey('services.Service', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[('Cash', 'Cash'), ('Card', 'Card'), ('Online', 'Online')])
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    received_by = models.ForeignKey('accounts.StaffProfile', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class LedgerEntry(models.Model):
    service= models.ForeignKey('services.Service', on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=[('Expense', 'Expense'), ('Payment', 'Payment')])
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey('accounts.StaffProfile', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Invoice(models.Model):
    service = models.ForeignKey('services.Service', on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=100, unique=True)
    invoice_date = models.DateTimeField(auto_now_add=True)
    sub_total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_number

