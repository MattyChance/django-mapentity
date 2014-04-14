from django.conf import settings
from django.conf.urls import patterns, url

from . import app_settings
from .views import (map_screenshot, convert, history_delete,
                    serve_secure_media, JSSettings)


_MEDIA_URL = settings.MEDIA_URL.replace(app_settings['ROOT_URL'], '')
if _MEDIA_URL.startswith('/'):
    _MEDIA_URL = _MEDIA_URL[1:]
if _MEDIA_URL.endswith('/'):
    _MEDIA_URL = _MEDIA_URL[:-1]


urlpatterns = patterns(
    '',
    url(r'^%s(?P<path>.*?)$' % _MEDIA_URL, serve_secure_media),
    url(r'^map_screenshot/$', map_screenshot, name='map_screenshot'),
    url(r'^convert/$', convert, name='convert'),
    url(r'^history/delete/$', history_delete, name='history_delete'),
    # See default value in app_settings.JS_SETTINGS.
    # Will be overriden, most probably.
    url(r'^api/settings.json$', JSSettings.as_view(), name='js_settings'),
)
