import mock
import unittest

from django.test.testcases import TestCase

from rest_framework_cache.cache import get_cache
from rest_framework_cache.registry import CacheRegistry
from rest_framework_cache.serializers import CachedSerializerMixin
from tests.serializers import TestSerializer2
from .serializers import TestSerializer
from .models import TestModel


class TestCachedSerializer(CachedSerializerMixin, TestSerializer):
    pass


class TestCachedSerializer2(CachedSerializerMixin, TestSerializer2):
    pass


class GetCacheKeyTestCase(TestCase):

    def setUp(self):
        self.registry = CacheRegistry()
        self.registry.register(TestCachedSerializer)
        self.registry.register(TestCachedSerializer2)

        self.instance = instance = TestModel()
        instance.id = 1000
        instance.save()
        self.serializer = TestCachedSerializer(instance)
        self.key = self.registry.get_cache_key(self.instance, TestCachedSerializer)
        self.expected_data = {"id": 1000, "name": ""}

    def test_cache_miss(self):
        with mock.patch.object(get_cache(), 'get', return_value=None) as get:
            with mock.patch.object(get_cache(), 'set') as set:
                with self.settings(REST_FRAMEWORK_CACHE={
                    'DEFAULT_CACHE_TIMEOUT': 5,
                }):
                    data = self.serializer.data

        self.assertEqual(data, self.expected_data)
        self.assertTrue(get.called)
        set.assert_called_with(self.key, self.expected_data, 5)

    def test_cache_hit(self):
        with mock.patch.object(get_cache(), 'get', return_value=self.expected_data) as get:
            with mock.patch.object(get_cache(), 'set') as set:
                data = self.serializer.data

        self.assertEqual(data, self.expected_data)
        self.assertTrue(get.called)
        self.assertFalse(set.called)

    def test_cache_clear(self):
        with mock.patch.object(get_cache(), 'get') as get,\
                mock.patch.object(get_cache(), 'set') as set, \
                mock.patch.object(get_cache(), 'delete') as delete:
            data = self.serializer.data

            self.assertEqual(delete.call_count, 0)
            self.instance.delete()
            self.assertEqual(delete.call_count, 2)  # 2 serializers




