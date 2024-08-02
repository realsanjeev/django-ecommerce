import io

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import View
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from address.models import Address
from payments.forms import CouponForm

from .forms import CheckoutForm
from .models import Order


@method_decorator(login_required, name="dispatch")
class OrderSummary(View):
    template_name = "order_summary.html"

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {"order": order}
            return render(
                self.request, template_name=self.template_name, context=context
            )
        except ObjectDoesNotExist:
            messages.warning(self.request, "You donot have an active order")
            return render(self.request, template_name=self.template_name, context={})


@method_decorator(login_required, name="dispatch")
class CheckoutView(View):
    template_name = "checkout.html"

    def get(self, *args, **kwargs):
        user = self.request.user
        try:
            order = Order.objects.get(user=user, ordered=False)
        except Order.DoesNotExist:
            messages.warning(self.request, "You donot have an active order")
            return redirect("/")
        form = CheckoutForm()
        context = {
            "form": form,
            "couponform": CouponForm(),
            "order": order,
            "DISPLAY_COUPON_FORM": True,
        }
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        user = self.request.user
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            """Procceed if only user have active order"""
        except ObjectDoesNotExist:
            messages.error("You donot have active order.")
            return redirect("order:checkout")
        if form.is_valid():
            cleaned_data = form.cleaned_data
            print("*" * 32)
            print(cleaned_data)
            print("*" * 32)
            street_address = form.cleaned_data.get("street_address")
            apartment_address = form.cleaned_data.get("apartment_address")
            country = form.cleaned_data.get("shipping_country")
            zip = form.cleaned_data.get("zip")
            payment_option = form.cleaned_data.get("payment_option")  # noqa
            billing_address = Address(
                user=user,
                street_address=street_address,
                apartment_address=apartment_address,
                country=country,
                zip=zip,
            )
            billing_address.save()
            order.billing_address = billing_address
            order.save()
            # REdirect to the selected payment option
            # for now stripe is only payment option
            return redirect("payment:payment-home")
        messages.error(self.request, "Failed to Checkout. Please try again Later!!!")
        return redirect("order:checkout")


@login_required
def history_view(request):
    template_name = "order-history.html"
    ordered_carts = Order.objects.filter(user=request.user, ordered=True)
    context = {"order_lists": ordered_carts}
    return render(request, template_name=template_name, context=context)


@login_required
def generate_history_pdf(request):
    # Create a file-like buffer to receive PDF data
    buffer = io.BytesIO()

    # Create the PDF object, using buffer as its file
    doc = SimpleDocTemplate(buffer, pagesize=letter, title="Order History")
    elements = []

    # Add title to the PDF
    title = "Real Django-Ecommerce"
    user = request.user.username
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    elements.append(Paragraph(title, title_style))
    elements.append(Paragraph(f"Email: {user}"))
    current_datetime = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    elements.append(Paragraph(f"Requested Date: {current_datetime}"))

    # Add a horizontal line
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("<hr/>", styles["Normal"]))

    # Prepare data for the table
    data = [
        ["Order ID", "Product", "Quantity", "Price"],  # Column headers
    ]

    # Retrieve orders for the current user
    orders = Order.objects.filter(user=request.user, ordered=True)

    # Populate table data with order details
    for order in orders:
        for ordered_product in order.products.all():
            data.append(
                [
                    str(order.id),
                    ordered_product.product.title,
                    str(ordered_product.quantity),
                    f"${ordered_product.get_total_product_price():.2f}",
                ]
            )

    # Create a Table object
    table = Table(data)

    # Add style to the Table
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ]
        )
    )

    # Add the table to the elements
    elements.append(Spacer(1, 12))  # Spacer to add space between the line and table
    elements.append(table)

    # Build the PDF
    doc.build(elements)

    # Seek to the beginning of the buffer
    buffer.seek(0)

    # Return the PDF as an HttpResponse with inline disposition
    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="history.pdf"'

    return response
