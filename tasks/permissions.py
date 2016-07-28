from rest_framework import permissions


class IsOwnerOrDelegate(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the task. Safe methods allowed to delegates
        if request.user in obj.delegates.all():

            if request.method in permissions.SAFE_METHODS:
                return True

        return obj.owner == request.user
