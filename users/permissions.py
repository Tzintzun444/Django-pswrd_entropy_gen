from rest_framework.permissions import BasePermission


class IsStaffOrAdmin(BasePermission):

    def has_permission(self, request, view):

        return request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)


class CustomUserPermission(BasePermission):

    def has_permission(self, request, view):

        if view.action == 'create':

            return True

        if view.action == 'list':

            return request.user.is_authenticated

        return True

    def has_object_permission(self, request, view, obj):

        if view.action in ['retrieve', 'destroy', 'update']:

            return obj.owner == request.user or request.user.is_staff or request.user.is_superuser

        return False
