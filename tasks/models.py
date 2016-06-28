from django.db import models


class Families(models.Model):
    user_id = models.ForeignKey('auth.User', related_name='Family')
    family_name = models.CharField(max_length=40)


class Task(models.Model):
    description = models.CharField(max_length=300)
    owner = models.ForeignKey('auth.User', related_name='Task')
    created_at = models.DateTimeField(auto_now_add=True)
    reactivated_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    repeatable = models.BooleanField(default=False)


class TaskList(models.Model):
    user_id = models.ForeignKey('auth.User', related_name="Tasks")
    task_id = models.ForeignKey(Task, related_name="Owner")

