from django.urls import path

from . import views
app_name = "search"
urlpatterns = [
    path("", views.search_list_view, name='product-search'),
    path('/product', views.search_by_category, name='product-by-category'),
]