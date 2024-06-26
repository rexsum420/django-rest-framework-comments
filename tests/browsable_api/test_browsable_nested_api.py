from django.test import TestCase
from django.test.utils import override_settings
from django.urls import path

<<<<<<< HEAD
from drf_comments import serializers
from drf_comments.generics import ListCreateAPIView
from drf_comments.renderers import BrowsableAPIRenderer
=======
from rest_framework import serializers
from rest_framework.generics import ListCreateAPIView
from rest_framework.renderers import BrowsableAPIRenderer
>>>>>>> e13688f0c0d32672d31ef3b9474c2a9f9dd12ae9


class NestedSerializer(serializers.Serializer):
    one = serializers.IntegerField(max_value=10)
    two = serializers.IntegerField(max_value=10)


class NestedSerializerTestSerializer(serializers.Serializer):
    nested = NestedSerializer()


class NestedSerializersView(ListCreateAPIView):
    renderer_classes = (BrowsableAPIRenderer, )
    serializer_class = NestedSerializerTestSerializer
    queryset = [{'nested': {'one': 1, 'two': 2}}]


urlpatterns = [
    path('api/', NestedSerializersView.as_view(), name='api'),
]


class DropdownWithAuthTests(TestCase):
    """Tests correct dropdown behaviour with Auth views enabled."""

    @override_settings(ROOT_URLCONF='tests.browsable_api.test_browsable_nested_api')
    def test_login(self):
        response = self.client.get('/api/')
        assert 200 == response.status_code
        content = response.content.decode()
        assert 'form action="/api/"' in content
        assert 'input name="nested.one"' in content
        assert 'input name="nested.two"' in content
