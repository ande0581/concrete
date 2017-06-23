from django.contrib import admin
from .models import Service


class ServiceModelAdmin(admin.ModelAdmin):
    list_display = ['category', 'description', 'cost', 'protected']
    ordering = ('category',)

admin.site.register(Service, ServiceModelAdmin)
