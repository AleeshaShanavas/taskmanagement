from rest_framework.permissions import BasePermission
from .constants import UserType

class IsAdminOrSuperAdmin(BasePermission):
    """
    Allows access only to admin and super admin users.
    """
    
    def has_permission(self, request, view):
        return request.user.role in [
            UserType.ADMIN,
            UserType.SUPER_ADMIN
        ]
