from django import forms

class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)


class CouponForm(forms.Form):
    code = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Promo code",
            "aria-label": "Recipient's username",
            "aria-describedby": "basic-addon2"
        }), label=False
    )
