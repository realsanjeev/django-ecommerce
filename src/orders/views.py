from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Order
from .forms import CheckoutForm
from address.models import Address
from payments.forms import CouponForm

@method_decorator(login_required, name='dispatch')
class OrderSummary(View):
    template_name = 'order_summary.html'

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'order': order
            }
            return render(self.request, template_name=self.template_name, context=context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You donot have an active order")
            return render(self.request, template_name=self.template_name, context={})

@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    template_name = 'checkout.html'
    def get(self, *args, **kwargs):
        user = self.request.user
        try:
            order = Order.objects.get(user=user, ordered=False)
        except Order.DoesNotExist:
            messages.warning(self.request, "You donot have an active order")
            return redirect('/')
        form = CheckoutForm()
        context = {
            'form': form,
            'couponform': CouponForm(),
            'order': order,
            'DISPLAY_COUPON_FORM': True
        }
        return render(self.request, self.template_name, context)
    
    def post(self, *args, **kwargs):
        user = self.request.user
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            '''Procceed if only user have active order'''
        except ObjectDoesNotExist:
            messages.error("You donot have active order.")
            return redirect('order:checkout')
        if form.is_valid():
            cleaned_data = form.cleaned_data
            print("*"*32)
            print(cleaned_data)
            print("*"*32)
            street_address = form.cleaned_data.get('street_address')
            apartment_address = form.cleaned_data.get('apartment_address')
            country = form.cleaned_data.get('shipping_country')
            zip = form.cleaned_data.get('zip')
            payment_option = form.cleaned_data.get('payment_option')
            billing_address = Address(user=user,
                                      street_address=street_address,
                                      apartment_address=apartment_address,
                                      country=country,
                                      zip=zip)
            billing_address.save()
            order.billing_address = billing_address
            order.save()
            # REdirect to the selected payment option
            # for now stripe is only payment option
            return redirect('payment:payment-home')
        messages.error(self.request, "Failed to Checkout. Please try again Later!!!")
        return redirect('order:checkout')
    
@login_required
def history_view(request):
    template_name = "order-history.html"
    ordered_carts = Order.objects.filter(user=request.user, ordered=True)
    context = {
        'order_lists': ordered_carts
    }
    return render(request, template_name=template_name, context=context)

@login_required
def pdf_history_view(request):
    pass

