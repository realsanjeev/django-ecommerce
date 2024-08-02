from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
    path('summary', views.OrderSummary.as_view(), name='order-summary'),
    path('checkout', views.CheckoutView.as_view(), name='checkout'),
    path('history', views.history_view, name="history"),
    path('history/pdf', views.generate_history_pdf, name="order-history"),

]