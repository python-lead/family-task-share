from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework.test import APIRequestFactory, APIClient, force_authenticate
from rest_framework import status
import json
from tasks.models import Task

from tasks.views import MyListApi


class MyListApiViewTest(TestCase):
    url_tasks = reverse('tasks')

    def setUp(self):

        # factory setup for tests
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='User1', password='c0mp1ic4t3dP@ssW05d111')

    def test_anonymous_user_view_access(self):
        # test assure that anonymous user doesn't have access to MyListApi view
        request = self.factory.get(self.url_tasks)
        request.user = AnonymousUser()
        response = MyListApi.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # I think i should test it against 401,
        # but i get 403 respond

    def test_logged_user_view_access(self):
        request = self.factory.get(self.url_tasks)
        request.user = self.user
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

        self.assertEqual(1, len(response.data))

    def test_get_non_existing_task(self):  # todo: make sure this test work properly
        request = self.factory.get(reverse('task', kwargs={'pk': 30}))
        request.user = User()  # AnonymousUser()
        response = MyListApi.as_view()(request)
        print 'test_get'
        print response.status_code
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    # def test_view_get_object(self):
    #     client = APIClient()
    #     client.login(username='User1', password='c0mp1ic4t3dP@ssW05d111')
    #     url = reverse('tasks:tasks')
    #     data = {'description': 'Take out the trash', 'repeatable': True}
    #     client.post(url, data, format='json')
    #
    #     task = MyListApi.get_object(id=1)
    #
    #     print task

