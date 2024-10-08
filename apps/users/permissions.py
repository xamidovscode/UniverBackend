from rest_framework.permissions import BasePermission
from . import models


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            return models.UserRoles.objects.filter(user=user, role='student').exists()
