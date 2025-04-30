from rest_framework import permissions


class DecanoPermissionClass(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET', 'OPTIONS', 'HEAD']:
            return request.user.has_perm('nucleo.view_nucleo')

        if request.method == 'POST':
            return request.user.has_perm('nucleo.add_nucleo')

        if request.method in ['PATCH', 'PUT']:
            return request.user.has_perm('nucleo.change_nucleo')

        if request.method == 'DELETE':
            return request.user.has_perm('nucleo.delete_nucleo')

        return False
