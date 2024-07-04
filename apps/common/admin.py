from django.contrib import admin
from ..common import models
# Register your models here.


@admin.register(models.Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", 'parent')
    list_display_links = ("id", "name", 'parent')


@admin.register(models.UserApartment)
class FloorAdmin(admin.ModelAdmin):
    list_display = ("id", "student", 'apartment')
    list_display_links = ("id", "student", 'apartment')


@admin.register(models.Attendance)
class FloorAdmin(admin.ModelAdmin):
    list_display = ("id", "student", 'apartment')
    list_display_links = ("id", "student", 'apartment')
