from django.shortcuts import render

from products.models import Product

def search_list_view(request):
    paginate_by = 4
    ordering = "title"

    q = request.GET.get('q', '')
    print("*"*45, q)
    
    if q is not None:
        results = Product.objects.search(q)
    else:
        results = None
    
    context = {
        "products": results
    }
    return render(request, "search.html", context)

def search_by_category(request):
    tags = request.GET.get('tags','')
    if tags:
        qs_products = Product.objects.search_by_tags('')
    else:
        qs_products = Product.objects.all()
    context = {
        "products": qs_products
    }
    return render(request, 'products.html', context)