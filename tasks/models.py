from django.db import models
from django.conf import settings


class Family(models.Model):  # todo: change name to family. Class names shouldn't be in plural form
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='Family')
    family_name = models.CharField(max_length=40)


class Task(models.Model):
    description = models.CharField(max_length=300)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='Task')
    created_at = models.DateTimeField(auto_now_add=True)
    reactivated_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    repeatable = models.BooleanField(default=False)
    delegate = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        return "[{}] owner {}, desc: {}".format(self.id,
                                                self.owner,
                                                self.description[:10])

    class Meta:
        ordering = ['-reactivated_at']

