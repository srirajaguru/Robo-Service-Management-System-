from django.db import models


class Notification(models.Model):
    TYPE_CHOICES = [
        ('Inward', 'Service Inward'),
        ('Completed', 'Service Completed'),
        ('Payment', 'Payment Received'),
        ('Custom', 'Custom Message'),
    ]

    STATUS_CHOICES = [
        ('Sent', 'Sent (API)'),
        ('Simulated', 'Simulated (Log)'),
        ('Failed', 'Failed'),
        ('Pending', 'Pending'),
    ]

    service = models.ForeignKey(
        'services.Service',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications'
    )
    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications'
    )
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Inward')
    phone_number = models.CharField(max_length=20)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    response_log = models.TextField(blank=True, default='')
    sent_by = models.ForeignKey(
        'accounts.StaffProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sent_at']
        verbose_name = 'WhatsApp Notification'
        verbose_name_plural = 'WhatsApp Notifications'

    def __str__(self):
        return f"{self.notification_type} to {self.phone_number} ({self.status}) - {self.sent_at:%d-%b %H:%M}"
