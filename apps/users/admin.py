from django.contrib import admin

from apps.users.models import User, UserRoles

admin.site.register(User)
admin.site.register(UserRoles)
