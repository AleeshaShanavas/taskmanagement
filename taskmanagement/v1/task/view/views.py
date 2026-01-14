from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from v1.task.models import Task
from v1.task.serializers import TaskSerializer, TaskCompletionSerializer
from v1.account.constants import UserType
from v1.task.constants import TaskStatus

@api_view(['GET'])
def get_user_tasks(request):
    """Retrieve tasks assigned to the authenticated user.
    # GET /tasks — only user's own tasks
    """

    tasks = Task.objects.filter(assigned_to=request.user)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
def update_task_status(request, id):
    """Update the status of a task assigned to the authenticated user.
    # PUT /tasks/{id} — update task status (with report if COMPLETED)
    """

    task = get_object_or_404(Task, id=id, assigned_to=request.user)
    
    new_status = request.data.get('status')
    if new_status == TaskStatus.COMPLETED:
        serializer = TaskCompletionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        task.status = TaskStatus.COMPLETED
        task.completion_report = serializer.validated_data['completion_report']
        task.worked_hours = serializer.validated_data['worked_hours']
    else:
        # Allow transition to PENDING or IN_PROGRESS without report
        if new_status in [TaskStatus.PENDING, TaskStatus.IN_PROGRESS]:
            task.status = new_status
        else:
            return Response(
                {'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
    task.save()
    return Response(TaskSerializer(task).data)


@api_view(['GET'])
def get_task_report(request, id):
    """Retrieve the completion report of a completed task.
    # GET /tasks/{id}/report — get task completion report (admin only)
    """
    if request.user.role not in [UserType.ADMIN, UserType.SUPER_ADMIN]:
        return Response(
            {'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    task = get_object_or_404(Task, id=id)
    if task.status != TaskStatus.COMPLETED:
        return Response(
            {'error': 'Task not completed'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        'completion_report': task.completion_report,
        'worked_hours': task.worked_hours,
        'task_title': task.title,
        'assigned_to': task.assigned_to.username,
    })

