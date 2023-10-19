from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('checkout', views.checkout_view, name='checkout'),
]