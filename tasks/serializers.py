from rest_framework import serializers
from tasks.models import Task
from datetime import datetime


# class TaskListSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = TaskList
#         fields = ('user_id', 'task_id')


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    reactivated_at = serializers.DateTimeField(default=datetime.now())

    class Meta:
        model = Task
        fields = ('id', 'description', 'created_at', 'reactivated_at', 'active', 'repeatable', 'owner')
