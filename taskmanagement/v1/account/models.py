from django.contrib.auth.models import AbstractUser
from django.db import models
from .constants import UserType

class CustomUser(AbstractUser):
    """Custom user model with role and assigned admin.
    
    Attributes:
        username (str): The username of the user.
        email (str): The email address of the user.
        role (int): The role of the user (Super Admin, Admin, User).
        assigned_admin (CustomUser): The admin assigned to this user 
            (if role is User).
    """

    role = models.IntegerField(
        choices=UserType.choices, default=UserType.USER)
    assigned_admin = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='users')

    def __str__(self):
        return self.username