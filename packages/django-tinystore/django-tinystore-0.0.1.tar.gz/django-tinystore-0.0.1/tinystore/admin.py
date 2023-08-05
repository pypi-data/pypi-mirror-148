from django.contrib import admin
from .models import TinyStore


@admin.register(TinyStore)
class TinyStoreAdmin(admin.ModelAdmin):
    list_display = ("key", "created", "last_update")
