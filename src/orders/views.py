from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Order
from .forms import CheckoutForm

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
            messages.warining(self.request, "You donot have an active order")
            return redirect('/')

@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    template_name = 'checkout.html'
    def get(self, *args, **kwargs):
        user = self.request.user
        order = Order.objects.get(user=user, ordered=False)
        form = CheckoutForm()
        context = {
            'form': form,
            'order': order
        }
        return render(self.request, self.template_name, context)
    
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        order = Order.objects.get(user=self.request.user, ordered=False)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            print("*"*32)
            print(cleaned_data)
            print("*"*32)
            return redirect('order:checkout')
        return redirect('order:checkout')

