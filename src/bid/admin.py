from django.contrib import admin
from .models import Bid


class BidModelAdmin(admin.ModelAdmin):
    list_display = ['description', 'customer_id', 'address_id', 'status', 'timestamp']

admin.site.register(Bid, BidModelAdmin)


