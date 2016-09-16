import unittest

from rest_framework_cache.registry import CacheRegistry
from tests.serializers import TestSerializer2

from .models import TestModel
from .serializers import TestSerializer


class GetCacheKeyTestCase(unittest.TestCase):

    def test_ok(self):
        instance = TestModel()
        instance.id = 1000
        serializer = TestSerializer()
        key = CacheRegistry.get_cache_key(instance, serializer.__class__)
        instance2 = TestModel(id=1000)
        serializer2 = TestSerializer()
        k2 = CacheRegistry.get_cache_key(instance2, serializer2.__class__)
        self.assertEqual(key, k2)

    def test_no_collisions(self):
        self.assertNotEqual(
            CacheRegistry.get_cache_key(TestModel(id=1), TestSerializer),
            CacheRegistry.get_cache_key(TestModel(id=2), TestSerializer)
        )
        self.assertNotEqual(
            CacheRegistry.get_cache_key(TestModel(id=1), TestSerializer),
            CacheRegistry.get_cache_key(TestModel(id=1), TestSerializer2)
        )


class GetAllCacheKeyTestCase(unittest.TestCase):

    def setUp(self):
        self.registry = CacheRegistry()
        self.registry.register(TestSerializer)
        self.registry.register(TestSerializer2)

    def test_ok(self):
        instance = TestModel(id=1000)
        keys = self.registry.get_all_cache_keys(instance)
        self.assertEqual(len(keys), 2)
        self.assertIn(
            CacheRegistry.get_cache_key(TestModel(id=1000), TestSerializer),
            keys
        )
        self.assertIn(
            CacheRegistry.get_cache_key(TestModel(id=1000), TestSerializer2),
            keys
        )

