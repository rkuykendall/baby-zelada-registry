from django.contrib import admin
from .models import Category, Item, Gift


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category", "quantity_desired")
    search_fields = ("name", "description")
    list_filter = ("category",)


class GiftAdmin(admin.ModelAdmin):
    list_display = ("giver_name", "gift_date")
    date_hierarchy = "gift_date"


admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Gift, GiftAdmin)
