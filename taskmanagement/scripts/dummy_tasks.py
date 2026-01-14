
from v1.task.models import Task
from datetime import date
from v1.task.constants import TaskStatus
from v1.account.models import CustomUser



# Get users
user1 = CustomUser.objects.get(username='user1')
user2 = CustomUser.objects.get(username='user2')
user3 = CustomUser.objects.get(username='user3')

# Create tasks
task1 = Task.objects.create(
    title="Setup Django Project",
    description="Initialize project structure and install dependencies.",
    assigned_to=user1,
    due_date=date(2026, 2, 1),
    status=TaskStatus.PENDING
)

task2 = Task.objects.create(
    title="Write API Docs",
    description="Document all task management endpoints.",
    assigned_to=user2,
    due_date=date(2026, 2, 5),
    status=TaskStatus.IN_PROGRESS
)

task3 = Task.objects.create(
    title="Test JWT Auth",
    description="Verify login and token refresh flow.",
    assigned_to=user1,
    due_date=date(2026, 1, 20),
    status=TaskStatus.IN_PROGRESS,
    completion_report="Successfully tested JWT login and protected routes.",
    worked_hours=3.5
)

task4 = Task.objects.create(
    title="Deploy to production",
    description="Deploy the project to a production environment.",
    assigned_to=user3,
    due_date=date(2026, 2, 10),
    status=TaskStatus.PENDING
)

task5 = Task.objects.create(
    title="Fix Security Vulnerabilities",
    description="Identify and fix security vulnerabilities in the project.",
    assigned_to=user2,
    due_date=date(2026, 2, 15),
    status=TaskStatus.IN_PROGRESS
)

print("Tasks created!")