from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from tasks import views


urlpatterns = [
    url(r'^mytasks/$', views.MyListApi.as_view()),
    url(r'^tasks/$', views.TaskListView.as_view()),
    url(r'^tasks/(?P<pk>[0-9]+)/$', views.TaskDetailView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
