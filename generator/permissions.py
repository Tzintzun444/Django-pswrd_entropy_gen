from rest_framework.permissions import BasePermission


class PasswordPermission(BasePermission):

    def has_permission(self, request, view):

        if view.action in ['list', 'create']:

            return request.user.is_authenticated

        return True

    def has_object_permission(self, request, view, obj):

        if view.action in ['destroy', 'retrieve']:

            return obj.owner == request.user or request.user.is_staff or request.user.is_superuser

        return False
