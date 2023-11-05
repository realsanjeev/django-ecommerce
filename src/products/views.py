from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from django.views.generic import ListView

from .models import Product
from orders.models import OrderProduct, Order

def product_detail(request, *args, **kwargs):
    template_name = "product-detail.html" 
    slug = kwargs.get("slug", None)
    product = Product.objects.get(slug=slug)
    context = {"product": product}
    return render(request, template_name, context)

def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    ordered_date = timezone.now()
    order_product, created = OrderProduct.objects.get_or_create(
        user=request.user,
        product=product,
        ordered=False)
    # get the cart of user or create if no cart for user
    order, order_created = Order.objects.get_or_create(user=request.user, ordered=False)

    # get number of quantity from form of product-detail
    if request.method=="POST":
        quantity = request.POST.get('quantity') or 1
        order_product.quantity = int(quantity)
        order_product.save()
        order.products.add(order_product)
        msg = f"Cart now has `{order_product.product.title.upper()}` with quantity {order_product.quantity}....."
        messages.success(request, message=msg)
        return redirect("order:order-summary")
    
    
    # check for product in cart and add + additional one product in cart
    if order.products.filter(product__slug=product.slug).exists():
        order_product.quantity += 1
        order_product.save()
        msg = f"Cart now has `{order_product.product.title.upper()}` with quantity {order_product.quantity}....."
        messages.success(request, message=msg)
        return redirect("order:order-summary")
    else:
        order.products.add(order_product)
        messages.info(request, "Product is added to cart....")
        return redirect("order:order-summary")


def decrease_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs.first()
        # check if the order product is in order
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            ).first()
            if order_product.quantity == 1:
                order.products.remove(order_product)
                # remove product from order and delete its instance
                order_product.delete()
                messages.warning(request, "This product is deleted from cart.")
            else:
                order_product.quantity -= 1
                msg = f"{order_product.product.title.upper()} is reduced by 1. Now total {order_product.product.title.upper()} is {order_product.quantity}"
                # save the updated instance of product in order
                order_product.save()
                messages.warning(request, msg)
            return redirect("order:order-summary")
        else:
            messages.error(request, "This item was not in your cart")
            return redirect("product:product-detail", slug=slug)
    else:
        messages.error(request, "You donot have an active order")
        return redirect("product:product-detail", slug=slug)

def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs.first()
        # check if the order product is in order
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            ).first()
            order.products.remove(order_product)
            # remove product from order and delete its instance
            order_product.delete()
            msg = f"Product `{order_product.product.title.upper()}` is deleted from cart."
            messages.warning(request, msg)
            return redirect("order:order-summary")
        else:
            messages.error(request, "This item was not in your cart")
            return redirect("product:product-detail", slug=slug)
    else:
        messages.error(request, "You donot have an active order")
        return redirect("product:product-detail", slug=slug)
    
class ProductsView(ListView):
    template_name = "products.html"
    model = Product
    paginate_by = 3
    # overrides objects_list key to user_defined key
    context_object_name = "products"
    # for consistent result in pagination
    ordering = ['title']
