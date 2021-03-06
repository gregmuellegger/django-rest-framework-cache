# django-rest-framework-cache

[![Build Status](https://travis-ci.org/yupeek/django-rest-framework-cache.svg?branch=master)](https://travis-ci.org/Onyo/django-rest-framework-cache)
[![Coverage Status](https://coveralls.io/repos/github/Yupeek/django-rest-framework-cache/badge.svg?branch=master)](https://coveralls.io/github/Yupeek/django-rest-framework-cache?branch=master)

DRF Cache provides easy to use, powerful and flexible cache framework for django-rest-framwork apps.


# Installation

Install using `pip`...

    pip install rest-framework-cache

Add `'rest_framework_cache'` to your `INSTALLED_APPS` setting.

```python
INSTALLED_APPS = (
    ...
    'rest_framework_cache',
)
```


# Requirements

This lib does not install any dependency, but your project obviously have to be using Django Rest Framework.

# compatibility

compatible with django 1.8, 1.9.
python 2.7, 3.4, 3.5


# Usage

To use the DRF cache you must register your serializer into cache 
registry to make sure the cache will be invalidated if the 
models is updated. 

You also must change your serializer to inherit the `CachedSerializerMixin` 
before the Serializer class:

```python
from rest_framework import serializers

# You must import the CachedSerializerMixin and cache_registry
from rest_framework_cache.serializers import CachedSerializerMixin
from rest_framework_cache.registry import cache_registry

from .models import Comment

@cache_registry.register
class CommentSerializer(CachedSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = Comment

```

# Configuration

To the cache successfully work you must configure the Django CACHES setting. We recomend that you take a look on Django cache docs here [https://docs.djangoproject.com/en/1.9/topics/cache/](https://docs.djangoproject.com/en/1.9/topics/cache/#setting-up-the-cache)


## Using a specific cache backend

If you need use a cache backend different of the default you can specify it on the `RF_CACHE_BACKEND`.

To do this edit your `settings.py` like this:

```python
# ...
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    },
    'rest_backend': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

REST_FRAMEWORK_CACHE = {
    'DEFAULT_CACHE_BACKEND': 'rest_backend',
}
# ...
```

## Cache timeout

You can set the cache timeout using `DEFAULT_CACHE_TIMEOUT`.

```python
REST_FRAMEWORK_CACHE = {
    'DEFAULT_CACHE_TIMEOUT': 86400, # Default is 1 day
}

```


# How it works

## Accessing the cache

When the representation of `CachedSerializerMixin` is called the fist thing that will be executed is a verification that checks if the request objects is already in cache, if yes the cached object will be returned without touch the database, otherwise the object will be requested to the database stored on cache and returned.


## Cleaning the cache

When your serializer is declareted using the `CachedSerializerMixin` the DRF cache register a signal to the serializer model. When a instance of the model has changed or deleted the signal clear related object on the cache backend.
