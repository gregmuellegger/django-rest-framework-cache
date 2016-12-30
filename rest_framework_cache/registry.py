from __future__ import unicode_literals

import hashlib

from django.db.models import signals
from django.utils.six import text_type
from rest_framework_cache.cache import get_cache

from .exceptions import AlreadyRegistered


class CacheRegistry:
    def __init__(self):
        self._registry = {}

    def register(self, serializer, model=None):
        """Store the serializer and model on registry to that the cache can be
        cleaned whenever an object is changed or deleted.
        After the serializer is registered we must connect the signals that
        clear the instance cache.
        can be used as a decorator
        """
        if model is None:
            model = serializer.Meta.model

        if model not in self._registry:
            self._registry[model] = []

        if serializer in self._registry[model]:
            raise AlreadyRegistered("Serializer {} is already registered"
                                    .format(model.__name__))

        self._registry[model].append(serializer)
        self.connect_signals(model)
        return serializer

    def connect_signals(self, model):
        signals.post_save.connect(self.clear_instance, sender=model)
        signals.pre_delete.connect(self.clear_instance, sender=model)

    def get(self, model):
        return self._registry.get(model, [])

    def get_all_cache_keys(self, instance):
        """Get all possibles cache keys for given instance"""
        keys = []
        serializers = self.get(instance.__class__)
        for serializer in serializers:
            keys.append(self.get_cache_key(instance, serializer))
        return keys

    @staticmethod
    def get_cache_key(instance, serializer):
        """Get cache key of instance"""
        return hashlib.sha256(".".join(text_type(o) for o in (
            instance.id,
            instance._meta.app_label,
            instance._meta.object_name,
            serializer.__name__
        )).encode('utf-8')).hexdigest()

    def clear_instance(self, sender, instance, **kwargs):
        """Calls cache cleaner for current instance"""
        keys = self.get_all_cache_keys(instance)
        get_cache().delete_many(keys)


cache_registry = CacheRegistry()
"""
global cache registry
"""
