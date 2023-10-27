from django.db import models
from django.conf import settings

from products.models import Product
from address.models import Address
from payments.models import Payment

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
            return self.get_total_orginal_product_price() - self.get_total_discounted_product_price()
        return 0
    
    class Meta:
        verbose_name_plural = "Order Product"
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(Address, related_name='shipping_address',
                                         on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(Address, related_name='billing_address',
                                        on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)

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
        return total
