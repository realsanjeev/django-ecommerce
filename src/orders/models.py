from django.db import models
from django.conf import settings

from products.models import Product

User = settings.AUTH_USER_MODEL
class OrderProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.quantity} of {self.product.title}"
    
    def get_total_product_price(self):
        return self.quantity * self.product.price
    
    class Meta:
        verbose_name_plural = "Order Product"
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date =models.DateTimeField()
    ordered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    

    def __str__(self):
        return self.user.email