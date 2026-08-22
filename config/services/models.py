from django.db import models
from customers.models import Customer

class Service(models.Model):
    service = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    device_type = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    complaint = models.TextField()
    physical_damage = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=10, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='Pending')
    expected_completion_date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey('accounts.StaffProfile', on_delete=models.SET_NULL, null=True, related_name='created_services')
    updated_by = models.ForeignKey('accounts.StaffProfile', on_delete=models.SET_NULL, null=True, related_name='updated_services')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ServiceHistory(models.Model):
    service= models.ForeignKey(Service, on_delete=models.CASCADE)
    old_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')])
    new_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed'),('Returned','Returned')])
    changed_by = models.ForeignKey('accounts.StaffProfile', on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)   

class ServiceProgress(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    progress_description = models.TextField()
    created_by = models.ForeignKey('accounts.StaffProfile', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

