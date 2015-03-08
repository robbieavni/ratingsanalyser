from django.conf.urls import patterns, url

from website import views

urlpatterns = patterns('',
    url(r'^(?P<user_id>[a-z]{2}\d{7})/$', views.user_detail, name='user-detail'),
    url(r'^new/$', views.UserView.as_view(), name='user-new'),
)