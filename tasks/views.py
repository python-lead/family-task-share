from rest_framework import generics
from tasks.models import Task
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


# class MyList(generics.ListCreateAPIView):
#     # todo: logout gives error int() argument must be a string or a number, not 'AnonymousUser'
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#
#     def filter_queryset(self, queryset):
#         queryset = Task.objects.all().filter(owner=self.request.user)
#         return queryset
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)


class MyListApi(APIView):
    """
    List all tasks created by user and all tasks delegated to him using APIView
    """

    def get(self, request, format=None):
        if self.request.user.id is None:  # todo: Find a better way to check if user is not 'AnonymousUser'
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        tasks = Task.objects.all().filter(Q(owner=self.request.user) | Q(delegate=self.request.user))
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):  # todo: get post method to work, make unavailable for anonymous users

        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
