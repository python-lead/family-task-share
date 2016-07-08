from rest_framework import generics
from tasks.models import Task
from tasks.serializers import TaskSerializer

from django.http import Http404
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


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
    permission_classes = (IsAuthenticated,)  # using permission_classes takes care of anonymous users accessing this
    #  view, but I need to understand how to change response on authentication failure from 403 to 401,
    # something about including WWW-Authenticate header

    def get(self, request, format=None):

        tasks = Task.objects.all().filter(Q(owner=self.request.user) | Q(delegate=self.request.user))
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):  # todo: get post method to work, make unavailable for anonymous users

        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['owner_id'] = request.user.id  # without this i get
            # IntegrityError: null value in column "owner_id" violates not-null constraint error
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
