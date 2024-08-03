from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django_countries.fields import CountryField

User = settings.AUTH_USER_MODEL
ADDRESS_CHOICES = (("B", "Billing"), ("C", "Shiping"))


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=128)
    apartment_address = models.CharField(max_length=128, null=True, blank=True)
    country = CountryField(multiple=False)
    zip = models.CharField(
        max_length=10,
        validators=[RegexValidator(r"^\d{5}$", message="Zip code must be 5 digits.")],
    )
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.street_address}"

    class Meta:
        verbose_name_plural = "Addresses"
