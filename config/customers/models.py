from django.db import models

class Customer(models.Model):
    customer = models.CharField(max_length=20, unique=True, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.customer:
            super().save(*args, **kwargs)
            self.customer = f"CUS-{self.created_at:%Y}-{self.pk:05d}"
            super().save(update_fields=["customer"])
            return
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
