from django.contrib import admin
from customer.models import Customer


class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'telephone', 'email']

admin.site.register(Customer, CustomerModelAdmin)
