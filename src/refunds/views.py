from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import RefundForm
from .models import Refund
from orders.models import Order

@method_decorator(decorator=login_required, name='dispatch')
class RefundRequestView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, 'request_refund.html', context=context)
    
    def post(self, *args, **kwargs):
        form =RefundForm(self.request.POST or None)
        if form.is_valid():
            print("*"*12)
            print(form.cleaned_data)
            print("*"*43)
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')

            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code, ordered=True)
                order.refund_request = True
                order.save()

                # store the refund
                refund = Refund(order=order, reason=message, email=email)
                refund.save()

                messages.info(self.request, "Your request was received. We will get back soon!!")
                return redirect('refund:request')
            except Order.DoesNotExist:
                messages.warning(self.request, "This order doesnot exist or order haven't hasnot checkout yet!!")
                return redirect('refund:request')

