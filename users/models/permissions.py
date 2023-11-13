from rest_framework.permissions import BasePermission


class ModeratorPermissions(BasePermission):
    def has_permission(self, request, view):
        # Проверяем, принадлежит ли пользователь группе "Модераторы"
        return request.user.groups.filter(name='модераторы').exists()


# Является ли пользователь владельцем
class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user == view.get_object().owner
