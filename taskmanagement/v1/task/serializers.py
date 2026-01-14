from rest_framework import serializers

from v1.task.models import Task

class TaskSerializer(serializers.ModelSerializer):
    """Serializer for task data. """

    assigned_to_username = serializers.ReadOnlyField(
        source='assigned_to.username')
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'assigned_to_username', 
            'due_date', 'status']


class TaskCompletionSerializer(serializers.Serializer):
    """Serializer for validating task completion data. """

    completion_report = serializers.CharField()
    worked_hours = serializers.DecimalField(max_digits=5, decimal_places=2)