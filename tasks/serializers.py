from rest_framework import serializers
from tasks.models import Task
from django.utils import timezone


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer class for tasks
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    reactivated_at = serializers.DateTimeField(default=timezone.now())  # changed from datetime.now to timezone.now

    class Meta:
        model = Task
        fields = ('id', 'description', 'created_at', 'reactivated_at', 'active', 'repeatable', 'owner', 'delegates')
