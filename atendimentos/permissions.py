from rest_framework import permissions


class AtenimentoPermissionClass(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET', 'OPTIONS', 'HEAD']:
            return request.user.has_perm('atenimento.view_atenimento')

        if request.method == 'POST':
            return request.user.has_perm('atenimento.add_atenimento')

        if request.method in ['PATCH', 'PUT']:
            return request.user.has_perm('atenimento.change_atenimento')

        if request.method == 'DELETE':
            return request.user.has_perm('atenimento.delete_atenimento')

        return False
