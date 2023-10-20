from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
    path('summary', views.OrderSummary.as_view(), name='order-summary'),
]