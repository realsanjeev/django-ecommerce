from django.urls import path
from . import views

app_name = "product"

urlpatterns = [
    path('<slug:slug>', views.product_detail, name="product-detail"),
    path('<slug:slug>/add-to-cart', views.add_to_cart, name="add-to-cart"),
    path('<slug:slug>/decrease-from-cart', views.decrease_from_cart, name='decrease-from-cart'),
    path('<slug:slug>/remove-from-cart', views.remove_from_cart, name='remove-from-cart')
]