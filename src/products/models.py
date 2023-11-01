from django.db import models
from django.db.models.query import Q, QuerySet
from django.shortcuts import reverse
from django.dispatch import receiver
from django.db.models.signals import pre_save

from ecommerce.utils import unique_slug_generator

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

class ProductQuerySet(models.QuerySet):
    def search(self, query):
        lookup = Q(title__icontains=query) | Q(description__icontains=query)
        qs = self.filter(lookup).distinct()
        return qs
    
    def search_by_tags(self, tags):
        return self.filter(category=tags)

class ProductManager(models.Manager):
    def get_queryset(self, *args, **kwargs) -> QuerySet:
        return ProductQuerySet(self.model, using=self._db)
    
    def search(self, query):
        return self.get_queryset().search(query)
    
    def search_by_tags(self, tags):
        return self.get_queryset().search_by_category(tags)

class Product(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(default=9.90, max_digits=8, decimal_places=2)
    discounted_price = models.DecimalField(default=0.00, max_digits=6, decimal_places=2)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField(null=True, blank=True, unique=True)
    image = models.ImageField(upload_to='product_images/')

    objects = ProductManager()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        # Replace the following line with your actual logic for generating the URL
        return reverse("product:product-detail", kwargs={'slug': self.slug})
    
    def get_add_to_cart_url(self):
        return reverse("product:add-to-cart", kwargs={'slug': self.slug})
    
    def get_decrease_from_cart_url(self):
        '''Decrease product quantity by 1'''
        return reverse("product:decrease-from-cart", kwargs={'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse("product:remove-from-cart", kwargs={'slug': self.slug})

@receiver(pre_save, sender=Product)
def product_pre_save_slug_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance=instance)