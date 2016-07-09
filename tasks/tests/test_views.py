from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework.test import APIRequestFactory, APIClient, force_authenticate
from rest_framework import status
import json
from tasks.models import Task

from tasks.views import MyListApi


class MyListApiViewTest(TestCase):
    def setUp(self):

        # factory setup for tests
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='User1', password='c0mp1ic4t3dP@ssW05d111')

    def test_anonymous_user_view_access(self):
        # test assure that anonymous user doesn't have access to MyListApi view
        request = self.factory.get(reverse('tasks:tasks'))
        request.user = AnonymousUser()
        response = MyListApi.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # I think i should test it against 401,
        # but i get 403 respond

    def test_logged_user_view_access(self):
        request = self.factory.get(reverse('tasks:tasks'))
        request.user = self.user
        response = MyListApi.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_post_as_anonymous(self):
        client = APIClient()
        url = reverse('tasks:tasks')
        data = {}
        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_post_as_authorised(self):
        client = APIClient()
        client.login(username='User1', password='c0mp1ic4t3dP@ssW05d111')
        url = reverse('tasks:tasks')
        data = {}
        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_create_task(self):
        client = APIClient()
        client.login(username='User1', password='c0mp1ic4t3dP@ssW05d111')
        url = reverse('tasks:tasks')
        data = {'description': 'Take out the trash', 'repeatable': True}
        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_task_list(self):
        client = APIClient()
        client.login(username='User1', password='c0mp1ic4t3dP@ssW05d111')
        url = reverse('tasks:tasks')
        data = {'description': 'Take out the trash', 'repeatable': True}
        client.post(url, data, format='json')
        response = client.get(url, format='json')

        self.assertEqual(1, len(response.data))
