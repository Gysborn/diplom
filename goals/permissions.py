from rest_framework import permissions

from goals.models import GoalComment


class CommentsPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj: GoalComment):
        return any((
            request.method in permissions.SAFE_METHODS,
            obj.user.id == request.user.id
        ))


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_id == request.user.id
