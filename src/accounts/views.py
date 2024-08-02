from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.generic import ListView

from products.models import Product


class HomeView(ListView):
    template_name = "home.html"
    model = Product
    paginate_by = 3
    # overrides objects_list key to user_defined key
    context_object_name = "products"
    # for consistent result in pagination
    ordering = ["image"]


@login_required
def checkout_view(request):
    template_name = "checkout.html"
    return render(request, template_name)


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")
