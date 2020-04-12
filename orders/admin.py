from django.contrib import admin
from . import models
import csv
from django.http import HttpResponse
import datetime
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.html import format_html

# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    raw_id_fields = ['product']


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;'\
        'filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many
              and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export to CSV'


def order_detail(obj):
    return mark_safe('<a href="{}">View</a>'.format(
        reverse('orders:admin_order_detail', args=[obj.id])))


def order_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(
        reverse('orders:admin_order_pdf', args=[obj.id])))


order_pdf.short_description = 'Invoice'


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated', order_detail, order_pdf]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]


def change_button(obj):
    return format_html('<a class="btn" href="/admin/orders/order/{}/change/">Change</a>', obj.id)


def delete_button(obj):
    return format_html('<a class="btn" href="/admin/orders/order/{}/delete/">Delete</a>', obj.id)


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'price',
                    'quantity', change_button, delete_button]
    raw_id_fields = ['order']
    list_editable = ['price', 'quantity']
    list_display_links = ['order']
