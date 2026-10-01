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

class IsEjecutivoOrEmpresaReadOnly(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return request.user.role in ["EJECUTIVO", "EMPRESA"]

        return request.user.role == "EJECUTIVO"