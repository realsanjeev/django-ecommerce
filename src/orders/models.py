from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from address.models import Address
from ecommerce.utils import generate_ref_code
from payments.models import Coupon, Payment
from products.models import Product

User = settings.AUTH_USER_MODEL


class OrderProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.quantity} of {self.product.title}"

    def get_total_orginal_product_price(self):
        return self.quantity * self.product.price

    def get_total_discounted_product_price(self):
        return self.quantity * self.product.discounted_price

    def get_total_product_price(self):
        if self.get_total_discounted_product_price() > 0:
            return self.get_total_discounted_product_price()
        else:
            return self.get_total_orginal_product_price()

    def get_saving(self):
        if self.get_total_discounted_product_price() > 0:
            return (
                self.get_total_orginal_product_price()
                - self.get_total_discounted_product_price()
            )
        return 0

    class Meta:
        verbose_name_plural = "Order Product"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=32)
    products = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        Address,
        related_name="shipping_address",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    billing_address = models.ForeignKey(
        Address,
        related_name="billing_address",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True
    )
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)

    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_request = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

    def get_total_price(self):
        total = 0
        for ordered_product in self.products.all():
            total += ordered_product.get_total_product_price()
        if self.coupon and total > self.coupon.amount:
            total -= self.coupon.amount
        return total


@receiver(
    pre_save,
    sender=Order,
)
def pre_save_ref_code_of_order(sender, instance, *args, **kwargs):
    if not instance.ref_code:
        instance.ref_code = generate_ref_code(instance)
