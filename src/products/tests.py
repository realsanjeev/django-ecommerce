from django.test import TestCase

from .models import Product

class ProductsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Product.objects.create(title='shirt', price=32.32535)

    def test_title_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_price_has_two_decimal(self):
        product = Product.objects.get(id=1)
        decimal_places = product._meta.get_field('price').decimal_places
        self.assertEqual(decimal_places, 2)

    def test_get_absolute_url(self):
        product = Product.objects.get(id=1)
        self.assertEqual(product.get_absolute_url(), '/product/shirt')
