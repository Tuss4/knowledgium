from rest_framework import permissions

class ContentPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated() and request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated() and request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated and request.user == obj.author:
            return True

        return request.user.is_staff


class CategoryPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated() and request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return self.has_permission()
