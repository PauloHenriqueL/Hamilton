from rest_framework import permissions


class DecanoPermissionClass(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET', 'OPTIONS', 'HEAD']:
            return request.user.has_perm('decano.view_decano')

        if request.method == 'POST':
            return request.user.has_perm('decano.add_decano')

        if request.method in ['PATCH', 'PUT']:
            return request.user.has_perm('decano.change_decano')

        if request.method == 'DELETE':
            return request.user.has_perm('decano.delete_decano')

        return False
