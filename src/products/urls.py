from django.urls import path
from . import views

app_name = "product"
urlpatterns = [
    path('<slug:slug>', views.product_detail, name="product-detail"),
]