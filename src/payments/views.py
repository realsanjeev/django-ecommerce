import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import View

from orders.models import Order

from .forms import CouponForm
from .models import Coupon, Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


def display_with_dashes(string):
    print("*" * 43)
    print(string)
    print("-" * 43)


@method_decorator(decorator=login_required, name="dispatch")
class PaymentView(View):
    def get(self, *args, **kwargs):
        user = self.request.user
        try:
            order = Order.objects.get(user=user, ordered=False)
        except Order.DoesNotExist:
            messages.warning(self.request, message="You donot have active order")
            return redirect("order:order-summary")
        context = {
            "order": order,
            "DISPLAY_COUPON_FORM": False,
            "STRIPE_PUBLISHABLE_KEY": settings.STRIPE_PUBLISHABLE_KEY,
        }
        return render(self.request, template_name="payment.html", context=context)

    def post(self, *args, **kwargs):
        user = self.request.user
        display_with_dashes(self.request.POST)
        try:
            order = Order.objects.get(user=user, ordered=False)
        except Order.DoesNotExist:
            messages.warning("There was no active order")
            return redirect("order:order-summary")
        stripe_token = self.request.POST.get("stripeToken")
        display_with_dashes(f"token: {stripe_token}")

        # do operatiion of registering userinfo and validating payment

        try:
            charge = stripe.Charge.create(
                amount=int(order.get_total_price() * 100),  # in cents
                currency="usd",
                source=stripe_token,
            )
            display_with_dashes(charge)
            # creating the payment
            payment = Payment()
            payment.stripe_charge_id = charge["id"]
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
            return redirect("/")
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get("error", {})
            print("[ERROR IN STRIPE]: ", err)
            messages.error(self.request, f"{e.user_message}")
            return redirect("/")
        except stripe.error.RateLimitError:
            messages.error(
                self.request, "Too many requests made to the API too quickly"
            )
            return redirect("/")
        except stripe.error.InvalidRequestError as e:
            display_with_dashes(e)
            messages.error(
                self.request, "Invalid parameters were supplied to Stripe's API"
            )
            return redirect("/")
        except stripe.error.AuthenticationError:
            messages.error(self.request, "Authentication with Stripe's API failed")
            return redirect("/")
        except stripe.error.APIConnectionError:
            messages.error(self.request, "Network communication with Stripe failed")
            return redirect("/")
        except stripe.error.StripeError:
            # Display a very generic error to the user, and maybe send
            messages.error(self.request, "Something went wrong. You are not charged")
            return redirect("/")
        except Exception:
            messages.error(
                self.request,
                "Sorry! We have been notified of your failure. Please try again later...",
            )
            return redirect("/")


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code, remaining_time__gt=1)
        return coupon
    except Coupon.DoesNotExist:
        messages.warning(request, "This token does not exist!!!")
        return redirect("order:checkout")


@method_decorator(decorator=login_required, name="dispatch")
class RedeemCouponView(View):
    def post(self, *args, **kwargs):
        display_with_dashes("Redeem coupon view")
        user = self.request.user
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get("code")
                order = Order.objects.get(user=user, ordered=False)
                coupon = get_coupon(self.request, code)
                # one order shuld be associated with only one coupon
                if order.coupon:
                    messages.info(self.request, "Coupon already assoiciated with order")
                    return redirect("order:checkout")
                order.coupon = coupon
                order.save()
                # decrease coupon remaining time
                order.coupon.remaining_time -= 1
                order.coupon.save()  # Fixed variable name here from 'coupon' to 'order.coupon'
                messages.success(self.request, "Successfully added coupon")
                return redirect("order:checkout")

            except Order.DoesNotExist:
                messages.warning(
                    self.request, "You don't have an active order to redeem a coupon"
                )  # Fixed typo here
                return redirect("order:checkout")  # Added return statement
