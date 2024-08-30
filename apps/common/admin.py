from django.contrib import admin
from ..common import models
# Register your models here.


@admin.register(models.Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", 'parent', 'is_active')
    list_display_links = ("id", "name", 'parent', 'is_active')


@admin.register(models.UserApartment)
class FloorAdmin(admin.ModelAdmin):
    list_display = ("id", "student", 'apartment')
    list_display_links = ("id", "student", 'apartment')


@admin.register(models.Attendance)
class FloorAdmin(admin.ModelAdmin):
    list_display = ("id", "student", 'apartment')
    list_display_links = ("id", "student", 'apartment')


@admin.register(models.Group)
class FloorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", 'teacher')
    list_display_links = ("id", "name", 'teacher')


@admin.register(models.LateReason)
class LateReasonAdmin(admin.ModelAdmin):
    list_display = ("id", "title", 'is_active')
    list_display_links = ("id", "title", 'is_active')


@admin.register(models.Application)
class ApplicationAdmin(admin.ModelAdmin):

    class DatesInline(admin.TabularInline):
        model = models.ApplicationDate

    inlines = [DatesInline]
    list_display = ("id", "user_apartment", 'admin')
    list_display_links = ("id", "user_apartment", 'admin')
