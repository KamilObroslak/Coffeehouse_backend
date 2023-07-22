from django.contrib import admin

from .models import Provider, OpenDayProvider, Coffee, Cake, Snacks, Place, Order, OrderHistory, OrderCoffee, OrderCake, \
    OrderSnacks, Product


class ProviderAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "owner", "kind", "city", "postcode", "street"]
    list_filter = ["kind", "city", "postcode"]
    search_fields = ["id", "name", "owner__username", "kind", "city", "postcode", "street"]
    readonly_fields = ["owner"]


class OpenDayProviderAdmin(admin.ModelAdmin):
    list_display = ["id", "owner"]
    list_filter = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    search_fields = ["id", "owner__username", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    readonly_fields = ["owner", "id"]


class CoffeeAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "owner", "price", "description", "gluten", "active"]
    list_filter = ["name", "gluten"]
    search_fields = ["id", "name", "price", "description", "gluten"]
    readonly_fields = ["id", "owner"]


class CakeAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "price", "description", "gluten"]
    list_filter = ["name", "gluten"]
    search_fields = ["id", "name", "price", "description", "gluten"]
    readonly_fields = ["id", "owner"]


class SnacksAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "price", "description", "gluten"]
    list_filter = ["name", "gluten"]
    search_fields = ["id", "name", "price", "description", "gluten"]
    readonly_fields = ["id", "owner"]


class PlaceAdmin(admin.ModelAdmin):
    list_display = ["id", "spot_amount", "name", "availability"]
    list_filter = ["spot_amount", "name", "availability"]
    search_fields = ["id", "spot_amount", "name", "availability"]
    readonly_fields = ["id"]


class OrderCoffeeInLine(admin.TabularInline):
    model = OrderCoffee
    autocomplete_fields = []
    extra = 0


class OrderCoffeeAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "coffee", "quantity"]
    list_filter = ["coffee", "quantity"]
    search_fields = ["order__id", "coffee__name", "quantity"]
    readonly_fields = ["order"]


class OrderCakeInLine(admin.TabularInline):
    model = OrderCake
    autocomplete_fields = []
    extra = 0


class OrderCakeAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "cake", "quantity"]
    list_filter = ["cake", "quantity"]
    search_fields = ["order__id", "cake__name", "quantity"]
    readonly_fields = ["order"]


class OrderSnacksInLine(admin.TabularInline):
    model = OrderSnacks
    autocomplete_fields = []
    extra = 0


class OrderSnacksAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "snacks", "quantity"]
    list_filter = ["snacks", "quantity"]
    search_fields = ["order__id", "snacks__name", "quantity"]
    readonly_fields = ["order"]


class OrderHistoryInLine(admin.TabularInline):
    model = OrderHistory
    autocomplete_fields = []
    extra = 0
    readonly_fields = ["order_id", "time_of_change", "status"]


class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ["id", "order_id", "time_of_change", "status"]
    list_filter = ["time_of_change", "status"]
    search_fields = ["order_id__id"]
    readonly_fields = ["order_id", "time_of_change"]


class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "owner", "total_price", "takeaway_order", "spot", "status", "order_datatime"]
    list_filter = ["spot", "takeaway_order", "status", "order_datatime"]
    search_fields = ["id", "owner__username", "total_price", "takeaway_order", "status", "spot__name"]
    inlines = [OrderCoffeeInLine, OrderCakeInLine, OrderSnacksInLine, OrderHistoryInLine]
    readonly_fields = ["id", "owner"]


class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "price", "description", "gluten", "owner", "active"]
    list_filter = ["gluten", "active"]
    search_fields = ["id", "name", "price", "gluten", "owner__username", "active"]
    readonly_fields = ["id", "owner"]


admin.site.register(Provider, ProviderAdmin)
admin.site.register(OpenDayProvider, OpenDayProviderAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Cake, CakeAdmin)
admin.site.register(Coffee, CoffeeAdmin)
admin.site.register(Snacks, SnacksAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderHistory, OrderHistoryAdmin)
admin.site.register(OrderCoffee, OrderCoffeeAdmin)
admin.site.register(OrderCake, OrderCakeAdmin)
admin.site.register(OrderSnacks, OrderSnacksAdmin)
admin.site.register(Product, ProductAdmin)
