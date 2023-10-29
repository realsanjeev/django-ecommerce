from django.contrib import admin
from .models import Address

class AdressAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'address_type',
                    'country',
                    'street_address',
                    'apartment_address',
                    'zip']
    list_filter = ['address_type', 'country']
    search_fields = ['user',
                    'zip',
                    'street_address',
                    'apartment_address']


admin.site.register(Address, AdressAdmin)