from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('checkout', views.checkout_view, name='checkout'),
]