from django.contrib import admin
from ..common import models
# Register your models here.


@admin.register(models.Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", 'parent')
    list_display_links = ("id", "name", 'parent')
