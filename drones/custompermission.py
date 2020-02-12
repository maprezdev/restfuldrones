# drones/custompermission.py file
from rest_framework import permissions


class IsCurrentUserOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """checks the HTTP verb in the request.method attribute"""
        if request.method in permissions.SAFE_METHODS:
            # the method is a safe method
            # grants permission to the request
            return True
        else:
            # The method isn't a safe method
            # Only owners are granted permissions for unsafe methods
            return obj.owner == request.user
