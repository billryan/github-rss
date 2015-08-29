from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('rss_gen.views',
    url(r'^(?P<owner>[\w,\-,\_]+)/(?P<repo>[\w,\-,\_]+)/.*$', 'feed_xml'),
    url(r'^$', 'index'),
)