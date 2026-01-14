from django.db import models
from v1.account.models import CustomUser
from v1.task.constants import TaskStatus

class Task(models.Model):
    """Model representing a task assigned to a user.

    Attributes:
        title (str): The title of the task.
        description (str): A detailed description of the task.
        assigned_to (CustomUser): The user to whom the task is assigned.
        due_date (date): The due date for the task completion.
        status (str): The current status of the task (
            Pending, In Progress, Completed).
        completion_report (str): A report detailing the completion of the task.
        worked_hours (Decimal): The number of hours worked on the task.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    due_date = models.DateField()
    status = models.CharField(
        max_length=20, choices=TaskStatus.choices, default=TaskStatus.PENDING)
    completion_report = models.TextField(null=True, blank=True)
    worked_hours = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.title
