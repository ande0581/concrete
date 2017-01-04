from django.contrib import admin
from customer.models import Customer


class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'company_name', 'telephone', 'email']

admin.site.register(Customer, CustomerModelAdmin)
