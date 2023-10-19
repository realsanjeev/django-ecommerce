from django.shortcuts import render

from products.models import Product
from address.models import Address

def home(request):
    context = {
        "products": Product.objects.all()
    }
    print(context)
    return render(request, 'home.html', context=context)

def checkout_view(request):
    template_name = 'checkout.html'
    return render(request, template_name)