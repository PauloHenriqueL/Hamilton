from rest_framework import permissions


class PacientePermissionClass(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET', 'OPTIONS', 'HEAD']:
            return request.user.has_perm('paciente.view_paciente')

        if request.method == 'POST':
            return request.user.has_perm('paciente.add_paciente')

        if request.method in ['PATCH', 'PUT']:
            return request.user.has_perm('paciente.change_paciente')

        if request.method == 'DELETE':
            return request.user.has_perm('paciente.delete_paciente')

        return False
