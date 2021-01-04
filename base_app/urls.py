from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
]

if settings.DEBUG:  # pragma: no cover
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns  # pylint: disable=ungrouped-imports
    urlpatterns += staticfiles_urlpatterns()
