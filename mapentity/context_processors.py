from django.conf import settings as settings_  # import the settings file

from . import app_settings, registry


def settings(request):
    return dict(
        TITLE=app_settings['TITLE'],
        DEBUG=settings_.DEBUG,
        VERSION=getattr(settings_, 'VERSION', 'unknown'),
        JS_SETTINGS_VIEW=app_settings['JS_SETTINGS_VIEW'],
        TRANSLATED_LANGUAGES=app_settings['TRANSLATED_LANGUAGES'],
        MAP_BACKGROUND_FOGGED=app_settings['MAP_BACKGROUND_FOGGED'],
        registry=registry,
    )
