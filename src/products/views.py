from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Product
from orders.models import OrderProduct, Order

def product_detail(request, *args, **kwargs):
    template_name = "product-detail.html"  # Adjust this path
    slug = kwargs.get("slug", None)
    product = Product.objects.get(slug=slug)
    context = {"product": product}
    return render(request, template_name, context)

def add_to_cart(request, slug):
    print("_"*43)
    print("*"*21, 'add to cart')
    product = get_object_or_404(Product, slug=slug)
    ordered_date = timezone.now()
    order_product, created = OrderProduct.objects.get_or_create(
        user=request.user,
        product=product,
        ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    # check if cart exists for user
    if order_qs.exists():
        order = order_qs.first()
        # check for product in cart
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity += 1
            order_product.save()
            return redirect("product:product-detail", slug=slug)
        else:
            order.products.add(order_product)
            return redirect("product:product-detail", slug=slug)
    else:
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.products.add(order_product)
        return redirect("product:product-detail", slug=slug)

