from rest_framework import permissions
from .models import *


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


class IsMessageOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        return obj.messaged_by == request.user

#
# class IsGroupMessage(permissions.BasePermission):
#
#     def has_object_permission(self, request, view, obj):
#
#         g = Group.objects.get.all()
#
#         return obj.group == g


# class IsGroupMember(permissions.BasePermission):
#
#     def has_permission(self, request, view):
#
#         user_obj = request.user
#
#         member = Group.objects.filter(members=user_obj)
#
#         if member:
#             return True
#         else:
#             return False

#
#
#
# class IsInGroup(permissions.BasePermission):
#
#     def has_object_permission(self, request, view, obj):
#
#         user_obj = request.user
#
#         member = Group.objects.filter(members=user_obj)
#
#         if member:
#             return True
