from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework import status
import json
from tasks.models import Task

from tasks.views import MyListApi, TaskDetailView


class MyListApiViewTest(TestCase):
    url_tasks = reverse('tasks')

    def setUp(self):

        # factory setup for tests
        self.factory = APIRequestFactory()
        self.user1 = User.objects.create_user(username='User1', password='c0mp1ic4t3dP@ssW05d111')
        self.user2 = User.objects.create_user(username='User2', password='c0mp1ic4t3dP@ssW05d111')
        # task = Task(description='Test task description', owner=self.user)
        # self.task = task.save()

    def test_anonymous_user_view_access(self):
        # test assure that anonymous user doesn't have access to MyListApi view
        request = self.factory.get(self.url_tasks)
        request.user = AnonymousUser()
        response = MyListApi.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # I think i should test it against 401,
        # but i get 403 respond

    def test_logged_user_view_access(self):
        request = self.factory.get(self.url_tasks)
        request.user = self.user1
        response = MyListApi.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_post_as_unauthorized(self):
        client = APIClient()
        # url = reverse('tasks:tasks')
        data = {}
        response = client.post(self.url_tasks, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_post_as_authorised(self):
        client = APIClient()
        client.login(username='User1', password='c0mp1ic4t3dP@ssW05d111')
        # url = reverse('tasks:tasks')
        # url = self.url
        data = {}
        response = client.post(self.url_tasks, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_create_task(self):
        client = APIClient()
        client.login(username='User1', password='c0mp1ic4t3dP@ssW05d111')
        # url = reverse('tasks:tasks')
        data = {'description': 'Take out the trash', 'repeatable': True}
        response = client.post(self.url_tasks, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_task_list(self):
        client = APIClient()
        client.login(username='User1', password='c0mp1ic4t3dP@ssW05d111')
        # url = reverse('tasks:tasks')
        data = {'description': 'Take out the trash', 'repeatable': True}
        client.post(self.url_tasks, data, format='json')
        response = client.get(self.url_tasks, format='json')
        # todo: research if i should use methods or views to get response

        self.assertEqual(1, len(response.data))

    def test_get_non_existing_task(self):  # todo: make sure this test work properly
        request = self.factory.get(reverse('task', kwargs={'pk': 1}))
        request.user = User()
        response = TaskDetailView.as_view()(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_task(self):
        client = APIClient()
        client.login(username='User1', password='c0mp1ic4t3dP@ssW05d111')
        data = {'description': 'User1 Task'}
        response = client.post(self.url_tasks, data, format='json')
        # response = client.get(reverse('task', kwargs={'pk': 2}), format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_existing_task_Forbidden(self):
        client = APIClient()
        client.login(username='User1', password='c0mp1ic4t3dP@ssW05d111')
        data = {'description': 'User1 Task'}
        client.post(self.url_tasks, data, format='json')

        client.login(username='User2', password='c0mp1ic4t3dP@ssW05d111')
        response = client.get(reverse('task', kwargs={'pk': 1}), format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_existing_task_Unauthorized(self):
        client = APIClient()
        client.login(username='User1', password='c0mp1ic4t3dP@ssW05d111')
        data = {'description': 'User1 Task'}
        client.post(self.url_tasks, data, format='json')

        request = self.factory.get(reverse('task', kwargs={'pk': 1}))
        request.user = AnonymousUser()
        response = TaskDetailView.as_view()(request, pk=1)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # todo: Raise 401 when user is Unauthorized

    def test_task_delete(self):  # This test stinks
        client = APIClient()
        client.login(username='User1', password='c0mp1ic4t3dP@ssW05d111')
        data = {'description': 'User1 Task'}
        client.post(self.url_tasks, data, format='json')

        response = client.get(self.url_tasks, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(1, len(response.data))


        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.delete(reverse('task', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # todo: I am not sure if this one works

        response = client.get(self.url_tasks, format='json')
        print '!!!!'
        print response.data
        self.assertEqual(0, len(response.data))


    # def test_task_delete_forbidden(self):
    #     client = APIClient()
    #     client.login(username='User1', password='c0mp1ic4t3dP@ssW05d111')
    #     data = {'description': 'User1 Task'}
    #     client.post(self.url_tasks, data, format='json')
    #     client.logout()
    #     client.login(username='User2', password='c0mp1ic4t3dP@ssW05d111')
    #
    #     response = client.get(reverse('task', kwargs={'pk': 1}))
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # This one gives 404
