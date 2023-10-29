from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

class Coupon(models.Model):
    code = models.CharField(max_length=16)
    amount = models.DecimalField(default=1.00, max_digits=5, decimal_places=2)
    remaining_time = models.IntegerField(default=1) 

    def __str__(self):
        return f"{self.code}"
