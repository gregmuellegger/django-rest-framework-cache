from django.core.cache import caches

from .settings import api_settings


def get_cache():
    return caches[api_settings.DEFAULT_CACHE_BACKEND]
