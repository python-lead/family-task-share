from django.contrib import admin
from .models import Task
# Register your models here.

admin.site.register(Task)


class TaskAdmin(admin.ModelAdmin):
    """
    Django admin custom settings
    """
    list_display = ('description'[:10],)
    search_fields = ('owner', 'active', 'repeatable', 'reactivated_at',)
    filter_horizontal = ('username', 'delegate')
