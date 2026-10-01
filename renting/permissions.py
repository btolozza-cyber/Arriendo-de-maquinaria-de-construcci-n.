from rest_framework.permissions import BasePermission

class IsEjecutivo(BasePermission):
    # Permite acceso solo a usuarios con rol EJECUTIVO

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "EJECUTIVO"
        )

class IsEmpresa(BasePermission):
    # Permite acceso solo a usuarios con rol de EMPRESA 

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "EMPRESA"
        )