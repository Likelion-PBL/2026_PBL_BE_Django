from django.contrib import admin
from .models import Lion, Task


@admin.register(Lion)
class LionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'track', 'created_at')
    search_fields = ('name', 'track')
    list_filter = ('track',)
    ordering = ('-created_at',)
    list_per_page = 20


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'lion', 'title', 'completed', 'created_at')
    list_filter = ('completed', 'lion__track')
    search_fields = ('title', 'lion__name')
    ordering = ('lion', 'created_at')
