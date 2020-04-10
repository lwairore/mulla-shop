from django.contrib import admin
from . import models

# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    raw_id_fields = ['product']


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
