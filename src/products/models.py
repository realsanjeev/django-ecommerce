from django.db import models
from django.shortcuts import reverse

CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Out wear')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

class Product(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    price = models.DecimalField(default=9.90, max_digits=8, decimal_places=2)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        # Replace the following line with your actual logic for generating the URL
        return reverse("product:product-detail", kwargs={'slug': self.slug})
    
    def get_add_to_cart_url(self):
        return reverse("product:add-to-cart", kwargs={'slug':self.slug})
