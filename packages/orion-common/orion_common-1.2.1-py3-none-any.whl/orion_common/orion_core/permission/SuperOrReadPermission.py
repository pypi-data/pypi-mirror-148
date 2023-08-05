from rest_framework import permissions


class SuperOrReadPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user['profile']['active']
        else:
            return bool(request.user['is_superuser'] and request['user']['profile']['active'])
