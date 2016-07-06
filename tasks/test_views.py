from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient, force_authenticate
# import json
from .models import Task

from .views import MyListApi


class MyListApiViewTest(TestCase):
    def setUp(self):

        # factory setup for tests
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='User1', password='c0mp1ic4t3dP@ssW05d111')

    def test_anonymous_user_view_access(self):
        # test assure that anonymous user doesn't have access to MyListApi view
        request = self.factory.get('/mytasks')
        request.user = AnonymousUser()
        response = MyListApi.as_view()(request)

        self.assertEqual(response.status_code, 401)

    def test_logged_user_view_access(self):
        request = self.factory.get('/mytasks')
        request.user = self.user
        response = MyListApi.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_post_method_create_task(self):
        request = self.factory.get('/mytasks')
        request.user = self.user

        client = APIClient()
        client.login(username='User1', password='c0mp1ic4t3dP@ssW05d111')
        force_authenticate(request, user=request.user)

        client.post('/mytasks/', {'description': 'Take out the trash', 'repeatable': True}, format='json')
        # ('id', 'description', 'created_at', 'reactivated_at', 'active', 'repeatable', 'owner')

        print Task.objects.all()

        response = self.client.get('/mytasks/')

        self.assertEqual(response.status_code, 201)  # I am getting 401 response status


