from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Provider, OpenDayProvider, Coffee, Cake, Snacks, Place, Order, OrderHistory, OrderCoffee, OrderCake, \
    OrderSnacks, Product


class OpenDayProviderInLine(admin.StackedInline):
    model = OpenDayProvider
    autocomplete_fields = []
    extra = 0
    fields = (('monday', 'monday_from', 'monday_to'),
              ('tuesday', 'tuesday_from', 'tuesday_to'),
              ('wednesday', 'wednesday_from', 'wednesday_to'),
              ('thursday', 'thursday_from', 'thursday_to'),
              ('friday', 'friday_from', 'friday_to'),
              ('saturday', 'saturday_from', 'saturday_to'),
              ('sunday', 'sunday_from', 'sunday_to'))


class OpenDayProviderAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "owner"]
    list_filter = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    search_fields = ["id", "owner__username", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday",
                     "sunday"]
    readonly_fields = ["owner", "id"]


class CoffeeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "name", "owner", "price", "description", "gluten", "active"]
    list_filter = ["name", "gluten"]
    search_fields = ["id", "name", "price", "description", "gluten"]
    readonly_fields = ["id", "owner"]


class CakeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "name", "price", "description", "gluten"]
    list_filter = ["name", "gluten"]
    search_fields = ["id", "name", "price", "description", "gluten"]
    readonly_fields = ["id", "owner"]


class SnacksAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "name", "price", "description", "gluten"]
    list_filter = ["name", "gluten"]
    search_fields = ["id", "name", "price", "description", "gluten"]
    readonly_fields = ["id", "owner"]


class PlaceInLine(admin.TabularInline):
    model = Place
    autocomplete_fields = []
    extra = 0


class PlaceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "owner", "spot_amount", "name", "availability"]
    list_filter = ["owner", "spot_amount", "name", "availability"]
    search_fields = ["id", "owner", "spot_amount", "name", "availability"]
    readonly_fields = ["id", "owner"]


class OrderCoffeeInLine(admin.TabularInline):
    model = OrderCoffee
    autocomplete_fields = []
    extra = 0


class OrderCoffeeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "order", "coffee", "quantity"]
    list_filter = ["coffee", "quantity"]
    search_fields = ["order__id", "coffee__name", "quantity"]
    readonly_fields = ["order"]


class OrderCakeInLine(admin.TabularInline):
    model = OrderCake
    autocomplete_fields = []
    extra = 0


class OrderCakeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "order", "cake", "quantity"]
    list_filter = ["cake", "quantity"]
    search_fields = ["order__id", "cake__name", "quantity"]
    readonly_fields = ["order"]


class OrderSnacksInLine(admin.TabularInline):
    model = OrderSnacks
    autocomplete_fields = []
    extra = 0


class OrderSnacksAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "order", "snacks", "quantity"]
    list_filter = ["snacks", "quantity"]
    search_fields = ["order__id", "snacks__name", "quantity"]
    readonly_fields = ["order"]


class OrderHistoryInLine(admin.TabularInline):
    model = OrderHistory
    autocomplete_fields = []
    extra = 0
    readonly_fields = ["order_id", "time_of_change", "status"]


class OrderHistoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "order_id", "time_of_change", "status"]
    list_filter = ["time_of_change", "status"]
    search_fields = ["order_id__id"]
    readonly_fields = ["order_id", "time_of_change", "status"]


class OrderInLine(admin.TabularInline):
    model = Order
    autocomplete_fields = []
    extra = 0
    readonly_fields = ["id", "spot", "total_price", "takeaway_order", "status",
                       "order_datatime", "provider"]


class OrderAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "owner", "total_price", "takeaway_order", "spot", "status", "order_datatime"]
    list_filter = ["spot", "takeaway_order", "status", "order_datatime"]
    search_fields = ["id", "provider__name", "total_price", "takeaway_order", "status", "spot__name"]
    inlines = [OrderCoffeeInLine, OrderCakeInLine, OrderSnacksInLine, OrderHistoryInLine]
    readonly_fields = ["id", "owner", "provider", "spot", "total_price", "status", "takeaway_order", "order_datatime"]
    fields = (("id", "owner", "provider", "total_price"), "spot", "status", "takeaway_order", "order_datatime")


class ProductInLine(admin.TabularInline):
    model = Product
    autocomplete_fields = []
    extra = 0


class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "name", "price", "description", "gluten", "owner", "active"]
    list_filter = ["gluten", "active"]
    search_fields = ["id", "name", "price", "gluten", "owner__username", "active"]
    readonly_fields = ["id", "owner"]


class ProviderAdmin(ImportExportModelAdmin ,admin.ModelAdmin):
    list_display = ["id", "name", "owner", "kind", "city", "postcode", "street"]
    list_filter = ["kind", "city", "postcode"]
    search_fields = ["id", "name", "owner__username", "kind", "city", "postcode", "street"]
    readonly_fields = ["owner", "kind"]
    inlines = [ProductInLine, PlaceInLine, OpenDayProviderInLine]
    actions = ["reminder"]
    fields = (("owner", "name", "kind"), ("city", "postcode", "street"),
              ("description", "facebook_link", "instagram_link"))

    def reminder(self, request, queryset):
        for provider in queryset:
            provider.reminder()
        self.message_user(request, "Send")

        # Definiujemy metodę obsługującą akcję

    def action(self, request, queryset):
        print("test")

    action.short_description = "Opcja nr 2"  # Tekst wyświetlany na przycisku akcji

    # Dodaj akcję do listy dostępnych akcji
    actions = ["action"]

    reminder.short_description = "Wyślij przypomnienie"



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
