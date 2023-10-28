import stripe
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.views.generic import View

from .models import Payment
from .forms import PaymentForm
from orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY

def display_with_dashes(string):
    print("*"*43)
    print(string)
    print("-"*43)

class PaymentView(View):
    def get(self, *args, **kwargs):
        user = self.request.user
        try:
            order = Order.objects.get(user=user, ordered=False)
        except Order.DoesNotExist:
            messages.warning(self.request, message="You donot have active order")
            return redirect('order:order-summary')
        context = {
            'order': order,
            'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY
        }
        return render(self.request, template_name='payment.html', context=context)
    
    def post(self, *args, **kwargs):
        user = self.request.user
        display_with_dashes(self.request.POST)
        try:
            order = Order.objects.get(user=user, ordered=False)
        except Order.DoesNotExist:
            messages.warning("There was no active order")
            return redirect('order:order-summary')
        form = PaymentForm(self.request.POST or None)
        stripe_token = self.request.POST.get('stripeToken')
        display_with_dashes(f"token: {stripe_token}")

        # do operatiion of registering userinfo and validating payment

        try:
            charge = stripe.Charge.create(
                amount=int(order.get_total_price() * 100), #in cents
                currency="usd",
                source=stripe_token
            )
            display_with_dashes(charge)
            # creating the payment
            payment = Payment()
            payment.stripe_charge_id =  charge['id']
            payment.amount = order.get_total_price()
            payment.user = user
            payment.save()

            # assign payment ito orders
            order_products = order.products.all()
            order_products.update(ordered=True)
            for product in order_products:
                product.save()
            
            order.ordered = True
            order.payment = payment
            order.save()

            messages.success(self.request, "Your order was successful!")
            return redirect('/')
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            messages.error(self.request, f"{e.user_message}")
            return redirect('/')
        except stripe.error.RateLimitError as e:
            messages.error(self.request, f"Too many requests made to the API too quickly")
            return redirect('/')
        except stripe.error.InvalidRequestError as e:
            display_with_dashes(e)
            messages.error(self.request, f"Invalid parameters were supplied to Stripe's API")
            return redirect('/')
        except stripe.error.AuthenticationError as e:
            messages.error(self.request, f"Authentication with Stripe's API failed")
            return redirect('/')
        except stripe.error.APIConnectionError as e:
            messages.error(self.request, f"Network communication with Stripe failed")
            return redirect('/')
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            messages.error(self.request, f"Something went wrong. You are not charged")
            return redirect('/')
        except Exception as e:
            messages.error(self.request, "Sorry! We have been notified of your failure. Please try again later...")
            return redirect('/')
    