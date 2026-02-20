from django.contrib import admin
from .models import Lion

@admin.register(Lion)
class LionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "track", "created_at")
    search_fields = ("name", "track")
    list_filter = ("track",)
    ordering = ("-created_at",)
    list_per_page = 10