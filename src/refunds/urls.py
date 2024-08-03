from django.urls import path

from . import views

app_name = "refund"
urlpatterns = [path("request", views.RefundRequestView.as_view(), name="request")]
