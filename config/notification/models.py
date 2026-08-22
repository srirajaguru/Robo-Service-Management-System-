from django.db import models
from accounts.models import StaffProfile
from services.models import Service

class Notification(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    customer= models.ForeignKey('customers.Customer', on_delete=models.CASCADE)
    notification_id = models.AutoField(primary_key=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=[('Pending', 'Pending'), ('Sent', 'Sent')], default='Pending') 
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(StaffProfile, on_delete=models.SET_NULL, null=True)
    sent_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name
