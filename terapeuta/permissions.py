from rest_framework import permissions


class PacientePermissionClass(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET', 'OPTIONS', 'HEAD']:
            return request.user.has_perm('terapeuta.view_terapeuta')

        if request.method == 'POST':
            return request.user.has_perm('terapeuta.add_terapeuta')

        if request.method in ['PATCH', 'PUT']:
            return request.user.has_perm('terapeuta.change_terapeuta')

        if request.method == 'DELETE':
            return request.user.has_perm('terapeuta.delete_terapeuta')

        return False
