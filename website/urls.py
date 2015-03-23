from django.conf.urls import patterns, url

from website import views

urlpatterns = patterns('',
    url(r'^details/(?P<pk>.*)/$', views.UserDetailView.as_view(), name='user-detail'),
    url(r'^create/$', views.UserCreateView.as_view(), name='user-create'),
)