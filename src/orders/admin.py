from django.contrib import admin
from .models import Order, OrderProduct

class OrderAdmin(admin.ModelAdmin):
    list_display = ["start_date", "ordered_date"]

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ["product", "quantity"]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
