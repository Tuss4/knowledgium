from rest_framework.permissions import BasePermission
from rest_framework import permissions


class CoderPermission(object):

    def has_permission(self, request, view):
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_authenticated and obj.email == user.email:
            return True

        return False
        
