from rest_framework import generics
from tasks.models import Task, TaskList
from tasks.serializers import TaskSerializer

from django.http import Http404
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class TaskListView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class MyList(generics.ListCreateAPIView):
    # todo: logout gives error int() argument must be a string or a number, not 'AnonymousUser'
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def filter_queryset(self, queryset):
        queryset = Task.objects.all().filter(owner=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MyListApi(APIView):
    """
    List all tasks created by user and all tasks delegated to him using APIView
    """

    def get(self, request, format=None):
        if self.request.user.id is None:  # todo: Find a better way to check if user is not 'AnonymousUser'
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        tasks = Task.objects.all().filter(owner=self.request.user)

        # delegated_task_id_list = TaskList.objects.all().filter(user_id=self.request.user.id)


        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
