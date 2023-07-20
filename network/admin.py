from django.contrib import admin
from django.utils.html import format_html

from .models import Contact, Product, NetworkNode


class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'country', 'city', 'street', 'house_number')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'release_date')


class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_supplier_link', 'debt', 'created_at')
    list_filter = ('contacts__city',)  # Фильтр по названию города
    actions = ['clear_debt']  # Добавляем действие очистки задолженности

    def get_supplier_link(self, obj):
        if obj.supplier:
            link = f'../../{obj.supplier._meta.app_label}/{obj.supplier._meta.model_name}/{obj.supplier.id}/change/'
            return format_html('<a href="{}">{}</a>', link, obj.supplier)
        return None

    get_supplier_link.allow_tags = True
    get_supplier_link.short_description = 'Поставщик'

    def clear_debt(self, request, queryset):
        # Административное действие для очистки задолженности перед поставщиком
        queryset.update(debt=0)

    clear_debt.short_description = 'Очистить задолженность'


admin.site.register(Contact, ContactAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(NetworkNode, NetworkNodeAdmin)
