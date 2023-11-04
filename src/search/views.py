from django.shortcuts import render

from products.models import Product, CATEGORY_CHOICES

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
    tags = request.GET.get('tag','').split(',')[0]
    qs_products = Product.objects.none()

    # convert tuples in dict
    category_dict = {
        'shirt': 'S',
        'sportwear': 'SW',
        'outwear': 'OW'
    }
    category_type = category_dict.get(tags, '')

    if tags:
        qs_products = Product.objects.filter(category__iexact=category_type)
    context = {
        "products": qs_products
    }
    return render(request, 'products.html', context)
