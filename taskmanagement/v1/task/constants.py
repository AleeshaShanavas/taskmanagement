from django.db import models
from django.utils.translation import gettext_lazy as _


class TaskStatus(models.TextChoices):
    """Enumeration for task status choices."""
    PENDING = 'PENDING', _('Pending')
    IN_PROGRESS = 'IN_PROGRESS', _('In Progress')
    COMPLETED = 'COMPLETED', _('Completed')