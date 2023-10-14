from django.shortcuts import render
from products.models import Product

def home(request):
    context = {
        "products": Product.objects.all()
    }
    print(context)
    return render(request, 'home.html', context=context)