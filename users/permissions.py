from rest_framework import permissions


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderators").exists()


class IsCreator(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.creator == request.user:
            return True
        return False