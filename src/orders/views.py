from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from .models import Order

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