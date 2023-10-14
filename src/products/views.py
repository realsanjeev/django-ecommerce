from django.shortcuts import render
from .models import Product

def product_detail(request, *args, **kwargs):
    template_name = "product.html"  # Adjust this path
    slug = kwargs.get("slug", None)
    print("*"*21, slug)
    product = Product.objects.get(slug=slug)
    context = {"product": product}
    return render(request, template_name, context)
