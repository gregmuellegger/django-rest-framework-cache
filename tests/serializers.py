from rest_framework.serializers import ModelSerializer

from .models import TestModel


class TestSerializer(ModelSerializer):

    class Meta:
        model = TestModel


class TestSerializer2(ModelSerializer):
    class Meta:
        model = TestModel
