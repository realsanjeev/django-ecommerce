from django.contrib import admin
from .models import Payment, Coupon

from refunds.models import Refund

class PaymentAdmin(admin.ModelAdmin):
    list_display = ["user", "stripe_charge_id", "amount"]
    list_display_links = ["user"]
    sortable_by = ["amount"]

class CouponAdmin(admin.ModelAdmin):
    list_display = ["code", "amount", "remaining_time"]
    sortable_by = ["amount", "remainig_time"]
    list_editable = ["remaining_time"]

class RefundAdmin(admin.ModelAdmin):
    list_display = ['order_ref_code', 'timestamp', 'reason', 'accepted', 'email']
    search_fields = ['email']
    sortable_by = ['timestamp']

    def order_ref_code(self, obj):
        return obj.order.ref_code

    order_ref_code.admin_order_field = 'order__ref_code'

admin.site.register(Payment, PaymentAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Refund, RefundAdmin)
