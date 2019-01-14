from rest_framework import permissions


class IsGroupAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.admin == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.username == request.user.username


class IsGroupMember(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        return obj.members == request.user.username


class IsMessageOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.messaged_by == request.user

