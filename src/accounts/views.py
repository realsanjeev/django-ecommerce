from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.generic import ListView

from products.models import Product
from address.models import Address

class HomeView(ListView):
    template_name = "home.html"
    model = Product
    paginate_by = 1
    # overrides objects_list key to user_defined key
    context_object_name = "products"
    # for consistent result in pagination
    ordering = ['image']


def checkout_view(request):
    template_name = 'checkout.html'
    return render(request, template_name)


def logout_view(request):
    logout(request)
    return redirect('login')