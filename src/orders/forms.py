from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (("S", "Stripe"), ("P", "PayPal"))


class CheckoutForm(forms.Form):
    street_address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "floatingInput",
            }
        ),
        strip=True,
    )

    apartmart_address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "floatingInput",
            }
        ),
        required=False,
        strip=True,
    )
    shipping_country = CountryField(blank_label="(select country)").formfield(
        required=False,
        widget=CountrySelectWidget(
            attrs={"class": "custom-select d-block w-100", "id": "country"}
        ),
    )
    zip = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "id": "zip"}),
        required=False,
    )

    same_shipping_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES, initial="S", disabled=True
    )
