from django.contrib import admin
from .models import Order, OrderProduct

def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)

make_refund_accepted.short_description = "Update orders to refund granted"

def make_begin_delivered_accepted(modeladmin, request, queryset):
    if queryset.filter(ordered=True).exists():
        queryset.update(being_delivered=True)

make_begin_delivered_accepted.short_description = "Update to being delivered"

def make_begin_delivered_accepted(modeladmin, request, queryset):
    if queryset.filter(being_delivered=True).exists():
        queryset.update(received=True)

make_begin_delivered_accepted.short_description = "Update to order received by customer"

class OrderAdmin(admin.ModelAdmin):
    list_display = ["user",
                    "ordered_date",
                    "ordered",
                    "being_delivered",
                    "received",
                    "refund_request",
                    "refund_granted",
                    "shipping_address",
                    "billing_address",
                    "payment",
                    "coupon"]

    list_display_links = ['user',
                        'shipping_address',
                        'billing_address',
                        'payment',
                        'coupon']

    search_fields = [
        'user__email',
        'ref_code'
    ]
    actions = [make_refund_accepted, make_begin_delivered_accepted]

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ["product", "quantity"]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
