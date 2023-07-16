from django.contrib import admin

from .models import Coffee, \
    Cake, \
    Order, \
    Place, \
    UserToken, \
    Snacks, \
    OrderCoffee, OrderCake, OrderSnacks


class UserTokenAdmin(admin.ModelAdmin):
    list_display = ["owner"]
    list_filter = ["owner"]


admin.site.register(Place)
admin.site.register(Coffee)
admin.site.register(Cake)
admin.site.register(Snacks)
admin.site.register(Order)
admin.site.register(OrderCoffee)
admin.site.register(OrderCake)
admin.site.register(OrderSnacks)

admin.site.register(UserToken, UserTokenAdmin)
