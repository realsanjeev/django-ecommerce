from django.db import models
from django.conf import settings
from django_countries.fields import CountryField

User = settings.AUTH_USER_MODEL
ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('C', 'Shiping')
)
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=128)
    apartmart_address = models.CharField(max_length=128)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=64)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email
    
    class Meta:
        verbose_name_plural = 'Addresses'