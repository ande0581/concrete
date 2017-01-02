from django.contrib import admin
from address.models import Address


class AddressModelAdmin(admin.ModelAdmin):
    list_display = ['street', 'city', 'state', 'zip', 'customer_id']

admin.site.register(Address, AddressModelAdmin)
