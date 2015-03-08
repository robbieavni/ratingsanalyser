from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ratingsanalyser.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'user/', include('website.urls')),
    url(r'^admin/', include(admin.site.urls)),

)