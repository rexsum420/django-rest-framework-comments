from django.test import TestCase

<<<<<<< HEAD
from drf_comments import serializers
=======
from rest_framework import serializers
>>>>>>> e13688f0c0d32672d31ef3b9474c2a9f9dd12ae9


class WriteOnlyFieldTests(TestCase):
    def setUp(self):
        class ExampleSerializer(serializers.Serializer):
            email = serializers.EmailField()
            password = serializers.CharField(write_only=True)

        self.Serializer = ExampleSerializer

    def test_write_only_fields_are_present_on_input(self):
        data = {
            'email': 'foo@example.com',
            'password': '123'
        }
        serializer = self.Serializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data == data

    def test_write_only_fields_are_not_present_on_output(self):
        instance = {
            'email': 'foo@example.com',
            'password': '123'
        }
        serializer = self.Serializer(instance)
        assert serializer.data == {'email': 'foo@example.com'}
