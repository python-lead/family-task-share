from rest_framework import generics, status
from tasks.models import Task
from tasks.serializers import TaskSerializer
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from tasks.permissions import IsOwnerOrDelegate
# from rest_framework.renderers import TemplateHTMLRenderer


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Show task details
    """
    permission_classes = (IsAuthenticated, IsOwnerOrDelegate,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class MyListApi(APIView):
    """
    List all tasks created by user and all tasks delegated to him using APIView
    """
    permission_classes = (IsAuthenticated,)  # using permission_classes takes care of anonymous users accessing this
    #  view, but I need to understand how to change response on authentication failure from 403 to 401,
    # something about including WWW-Authenticate header

    # renderer_classes = [TemplateHTMLRenderer]  # todo: Figure out how to make template renderer work, tests don't pass
    # template_name = 'tasks/mytasks.html'

    def get(self, request, format=None):

        tasks = Task.objects.all().filter(Q(owner=self.request.user) | Q(delegates=self.request.user))
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['owner_id'] = request.user.id  # without this i get
            # IntegrityError: null value in column "owner_id" violates not-null constraint error
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



