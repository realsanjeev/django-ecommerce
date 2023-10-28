from django.urls import path
from . import views

app_name = 'payment'
urlpatterns = [
    path('', views.PaymentView.as_view(), name="payment-home"),
]
