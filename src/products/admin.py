from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'label']

admin.site.register(Product, ProductAdmin)
