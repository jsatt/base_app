from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

try:
    from local_urls import urlpatterns as local_urls
except ImportError:
    pass
else:
    urlpatterns += local_urls
