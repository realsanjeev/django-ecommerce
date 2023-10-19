from django.urls import path
from . import views

app_name = "product"

urlpatterns = [
    path('<slug:slug>', views.product_detail, name="product-detail"),
    path('<slug:slug>/add-to-cart', views.add_to_cart, name="add-to-cart"),
]