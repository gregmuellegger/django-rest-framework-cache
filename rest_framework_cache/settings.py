"""
Settings for REST framework cache are all namespaced in the
REST_FRAMEWORK_CACHE setting. For example your project's `settings.py` file
might look like this:

REST_FRAMEWORK_CACHE = {
    'DEFAULT_CACHE_TIMEOUT': 86400
}

This module provides the `api_setting` object, that is used to access
REST framework cache settings, checking for user settings first, then falling
back to the defaults.
"""
from __future__ import unicode_literals

from django.conf import settings
from django.test.signals import setting_changed


DEFAULTS = {
    'DEFAULT_CACHE_BACKEND': 'default',
    'DEFAULT_CACHE_TIMEOUT': 86400,
    'SERIALIZER_CACHE_KEY_FORMAT': '{protocol}.{app_label}.{model_name}.'
                                   '{serializer_name}:{id}',

}


class APISettings(object):

    """
    A settings object, that allows API settings to be accessed as properties.
    For example:

        from rest_framework_cache.settings import api_settings
        print(api_settings.DEFAULT_CACHE_TIMEOUT)

    """

    def __init__(self, defaults=None):
        self.defaults = defaults
        self._settings = {}
        self.reload()

    def reload(self):
        self._settings = self.defaults.copy()
        self._settings.update(getattr(settings, 'REST_FRAMEWORK_CACHE', {}))

    def __getattr__(self, attr):
        return self._settings[attr]


api_settings = APISettings(DEFAULTS)


def reload_api_settings(setting, *args, **kwargs):
    if setting == 'REST_FRAMEWORK_CACHE':
        api_settings.reload()


setting_changed.connect(reload_api_settings)
