from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework import status
import json

from tasks.views import MyListApi, TaskDetailView


class MyListApiViewTest(TestCase):
    """
    TestCase class covering:
    'tasks' view:

        test_anonymous_user_view_access
        test_logged_user_view_access
        test_invalid_post_as_unauthorized
        test_invalid_post_as_authorised
        test_post_create_task
        test_task_list

    'task/{task_id}' view:

        test_get_non_existing_task
        test_get_task
        test_get_existing_task_Forbidden
        test_get_existing_task_Unauthorized
        test_task_delete
        test_task_delete_forbidden
        test_update_existing_task
        test_update_task_unauthorized

    'task/{task_id}' view as delegate

        test_delegate_get_task
        test_delegate_put_task_unauthorized
        test_delegate_delete_task_unauthorized

    Test coverage not yet implemented:
        -
    """

    def setUp(self):

        # factory setup for tests
        self.url_tasks = reverse('tasks')
        self.factory = APIRequestFactory()
        self.password = 'c0mp1ic4t3dP@ssW05d111'
        self.user1 = User.objects.create_user(username='User1', password=self.password)
        self.user2 = User.objects.create_user(username='User2', password=self.password)

    def create_logged_client(self, user):
        client = APIClient()
        client.login(username=user, password=self.password)
        return client

    def test_anonymous_user_view_access(self):
        # test assure that anonymous user doesn't have access to MyListApi view
        """
        Testing if unauthorized user can't access 'tasks' view
        """
        request = self.factory.get(self.url_tasks)
        request.user = AnonymousUser()
        response = MyListApi.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # I think i should test it against 401,
        # but i get 403 respond

    def test_logged_user_view_access(self):
        """
        Testing if authorized user can access 'tasks' view
        """
        request = self.factory.get(self.url_tasks)
        request.user = self.user1
        response = MyListApi.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_post_as_unauthorized(self):
        """
        Testing if unauthorized can't create new task
        """
        client = APIClient()
        data = {}
        response = client.post(self.url_tasks, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_post_as_authorised(self):
        """
        Testing if authorized user can't create new task with wrong data
        """
        client = self.create_logged_client('User1')
        data = {}  # todo: this test needs further validations
        response = client.post(self.url_tasks, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_create_task(self):
        """
        Testing if authorized user can create new task
        """
        client = self.create_logged_client('User1')
        data = {'description': 'Take out the trash', 'repeatable': True}
        response = client.post(self.url_tasks, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_task_list(self):
        """
        Testing if creating tasks properly increment the amount of tasks owned by user
        """
        client = self.create_logged_client('User1')
        data = {'description': 'Take out the trash', 'repeatable': True}
        client.post(self.url_tasks, data, format='json')
        client.post(self.url_tasks, data, format='json')
        response = client.get(self.url_tasks, format='json')
        # todo: research if i should use methods or views to get response

        self.assertEqual(2, len(response.data))

    def test_get_non_existing_task(self):
        """
        Testing if user get 404 when requesting not existing task
        """
        request = self.factory.get(reverse('task', kwargs={'pk': 1}))
        request.user = User()
        response = TaskDetailView.as_view()(request, pk=1)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_task(self):
        """
        Testing if User can request task detail for his existing task
        """
        client = self.create_logged_client('User1')
        data = {'description': 'User1 Task'}
        pk = client.post(self.url_tasks, data, format='json').data['id']
        response = client.get(reverse('task', kwargs={'pk': pk}), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_existing_task_Forbidden(self):
        """
        Testing if user can't access tasks he is not allowed to
        """
        client = self.create_logged_client('User1')
        data = {'description': 'User1 Task'}
        pk = client.post(self.url_tasks, data, format='json').data['id']
        client.login(username='User2', password='c0mp1ic4t3dP@ssW05d111')
        response = client.get(reverse('task', kwargs={'pk': pk}), format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_existing_task_Unauthorized(self):
        """
        Testing if user can't access a task then he is unauthorized (not logged in)
        """
        client = self.create_logged_client('User1')
        data = {'description': 'User1 Task'}
        pk = client.post(self.url_tasks, data, format='json').data['id']

        request = self.factory.get(reverse('task', kwargs={'pk': pk}))
        request.user = AnonymousUser()
        response = TaskDetailView.as_view()(request, pk=pk)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # todo: Raise 401 when user is Unauthorized

    def test_task_delete(self):  # This test stinks
        """
        Testing if user can delete a task he owns
        """
        client = self.create_logged_client('User1')
        data = {'description': 'User1 Task'}
        pk = client.post(self.url_tasks, data, format='json').data['id']
        client.get(self.url_tasks, format='json')
        response = client.delete(reverse('task', kwargs={'pk': pk}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_task_delete_forbidden(self):
        """
        Testing if user can't delete a task he doesn't own
        """
        client = self.create_logged_client('User1')
        data = {'description': 'User1 Task'}
        pk = client.post(self.url_tasks, data, format='json').data['id']
        client.logout()
        client = self.create_logged_client('User2')
        response = client.get(reverse('task', kwargs={'pk': pk}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_existing_task(self):
        """
        Testing if authorized user can update a task using .put method
        """
        client = self.create_logged_client('User1')
        data = {'description': 'This is old description', 'repeatable': False}
        pk = client.post(self.url_tasks, data=data, format='json').data['id']
        new_data = {'description': 'This is old description', 'repeatable': True}
        response = client.put(reverse('task', kwargs={'pk': pk}), data=new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get(reverse('task', kwargs={'pk': pk}))

        self.assertEqual(json.loads(response.content)['description'], new_data['description'])

    def test_update_task_unauthorized(self):
        """
        Testing if unauthorized user can't update an task
        """
        client = self.create_logged_client('User1')
        data = {'description': 'This is old description', 'repeatable': False}
        pk = client.post(self.url_tasks, data=data, format='json').data['id']
        client.logout()
        client.login(username='User2', password=self.password)
        new_data = {'description': 'This is old description', 'repeatable': True}
        response = client.put(reverse('task', kwargs={'pk': pk}), data=new_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     things to test as delegate - post with delegate, get, put, delete

    def test_delegate_get_task(self):
        """
        Testing if delegates can access tasks which they are allowed
        """
        client = self.create_logged_client('User1')
        data = {'description': 'This is User1 task delegated to User2', 'delegates': [self.user2.id]}
        pk = client.post(self.url_tasks, data).data['id']
        client.logout()
        client.login(username='User2', password=self.password)
        response = client.get(reverse('task', kwargs={'pk': pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delegate_put_task_unauthorized(self):
        """
        Testing if delegates can't update tasks which they are allowed
        """
        client = self.create_logged_client('User1')
        data = {'description': 'This is User1 task delegated to User2', 'delegates': [self.user2.id]}
        pk = client.post(self.url_tasks, data).data['id']
        client.logout()
        client.login(username='User2', password=self.password)
        response = client.put(reverse('task', kwargs={'pk': pk}), data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delegate_delete_task_unauthorized(self):
        """
        Testing if delegates can't delete tasks which they are allowed
        """
        client = self.create_logged_client('User1')
        data = {'description': 'This is User1 task delegated to User2', 'delegates': [self.user2.id]}
        pk = client.post(self.url_tasks, data).data['id']
        client.logout()
        client.login(username='User2', password=self.password)
        response = client.delete(reverse('task', kwargs={'pk': pk}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)







