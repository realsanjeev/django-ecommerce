from django.db import models

from orders.models import Order


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self) -> str:
        return f"{self.pk} - {self.email}"