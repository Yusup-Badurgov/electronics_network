from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class CustomPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        _filters: dict = {'user_id': request.user.id, 'is_active': request.user.is_active}

        if request.method not in SAFE_METHODS:
            return _filters['is_active']

        return _filters['is_active']
