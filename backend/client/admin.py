from django.contrib import admin

from client.models import Client


class ClientAdmin(admin.ModelAdmin):
    list_display = ["id", "owner", "phone", "city", "postcode", "street"]
    list_filter = ["city", "postcode"]
    search_fields = ["owner__username", "phone", "city", "postcode", "street"]
    readonly_fields = ["id", "owner"]


admin.site.register(Client, ClientAdmin)
