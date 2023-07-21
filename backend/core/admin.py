from django.contrib import admin

from core.models import UserToken


class UserTokenAdmin(admin.ModelAdmin):
    list_display = ["id", "owner"]
    search_fields = ["id", "owner"]


admin.site.register(UserToken, UserTokenAdmin)
