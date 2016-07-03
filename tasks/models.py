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

    def __str__(self):
        return "[{}] owner {}, desc: {}".format(self.id,
                                                self.owner,
                                                self.description[:10])

    class Meta:
        ordering = ['-reactivated_at']


class TaskList(models.Model):
    # todo: change user_id, task_id names to user, task. make migrations
    # todo: owner shouldn't be allowed to delegate task to himself
    user_id = models.ForeignKey('auth.User', related_name="Tasks")
    task_id = models.ForeignKey(Task, related_name="Owner")

    def __str__(self):
        return "[{}] owner {}, delegate {}, desc: {}".format(self.task_id.id,
                                                             self.task_id.owner,
                                                             self.user_id.username,
                                                             self.task_id.description[:10])
