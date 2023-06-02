from django.contrib import admin

from .models import URL


class URLAdmin(admin.ModelAdmin):
    list_display = "user", "url", "paused"


admin.site.register(URL, URLAdmin)
