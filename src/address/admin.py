from django.contrib import admin
from .models import Address

class AdressAdmin(admin.ModelAdmin):
    list_display = ['user', 'country', 'address_type']

admin.site.register(Address, AdressAdmin)