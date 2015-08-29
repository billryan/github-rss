from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'github_rss.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'github.views.index'),
    url(r'^github/', include('github.urls')),
    url(r'^feed/', include('rss_gen.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

from celerytask.views import Hello
urlpatterns += patterns('',url(r'^celery/',Hello.as_view()),)
