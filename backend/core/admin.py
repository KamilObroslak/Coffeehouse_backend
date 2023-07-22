from django.contrib import admin

from core.models import UserToken


class UserTokenAdmin(admin.ModelAdmin):
    list_display = ["id", "owner", "token"]
    search_fields = ["id", "owner", "token"]
    readonly_fields = ["id", "owner", "token"]


admin.site.register(UserToken, UserTokenAdmin)
