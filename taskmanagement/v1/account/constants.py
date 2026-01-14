from django.db import models
from django.utils.translation import gettext_lazy as _


class UserType(models.IntegerChoices):
    """Enumeration for user role types."""
    
    SUPER_ADMIN = 101, _('Super Admin')
    ADMIN = 102, _('Admin')
    USER = 103, _('User')
