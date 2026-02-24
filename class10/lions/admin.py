from django.contrib import admin
from .models import Lion, Task

@admin.register(Lion)
class LionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "track", "created_at")
    search_fields = ("name", "track")
    list_filter = ("track",)
    ordering = ("-created_at",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "lion", "completed", "created_at")
    list_filter = ("completed",)
    search_fields = ("title",)
    ordering = ("-created_at",)