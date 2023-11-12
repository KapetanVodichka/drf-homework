from rest_framework.permissions import BasePermission

from users.models import UserRole


class IsMember(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == UserRole.Member:
            return True


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == UserRole.Moderator:
            return True