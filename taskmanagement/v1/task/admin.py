from django.contrib import admin

# Register your models here.
from v1.task.models import Task

admin.site.register(Task)