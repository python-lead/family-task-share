from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework.test import APIRequestFactory, APIClient, force_authenticate
# import json
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

        self.assertEqual(response.status_code, 403)  # I think i should test it against 401, but i get 403 respond

    def test_logged_user_view_access(self):
        request = self.factory.get(reverse('tasks:tasks'))
        request.user = self.user
        response = MyListApi.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_invalid_post_as_anonymous(self):
        request = self.factory.post(reverse('tasks:tasks'), {})
        view = MyListApi.as_view()
        response = view(request)
        response.render()
        self.assertEqual(response.status_code, 403)

    def test_invalid_post_as_authorised(self):
        client = APIClient()
        client.login(username='User1', password='c0mp1ic4t3dP@ssW05d111')

        request = client.post(reverse('tasks:tasks'), {})
        view = MyListApi.as_view()
        response = view(request)
        response.render()

        self.assertEqual(response.status_code, 400)

    def test_post_create_task(self):
        client = APIClient()
        client.login(username='User1', password='c0mp1ic4t3dP@ssW05d111')

        request = client.post(reverse('tasks:tasks'), {'description': 'Take out the trash', 'repeatable': True},
                              format='json')
        # ('id', 'description', 'created_at', 'reactivated_at', 'active', 'repeatable', 'owner')

        view = MyListApi.as_view()
        response = view(request)
        response.render()
        self.assertEqual(response.status_code, 201)  # I am getting 401 response status


