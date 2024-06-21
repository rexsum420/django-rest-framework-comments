<<<<<<< HEAD
from drf_comments.serializers import ModelSerializer
=======
from rest_framework.serializers import ModelSerializer
>>>>>>> e13688f0c0d32672d31ef3b9474c2a9f9dd12ae9
from tests.models import BasicModelWithUsers


class BasicSerializer(ModelSerializer):
    class Meta:
        model = BasicModelWithUsers
        fields = '__all__'
