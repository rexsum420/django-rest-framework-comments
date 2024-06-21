from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import override_settings
from django.urls import path

<<<<<<< HEAD
from drf_comments.authentication import TokenAuthentication
from drf_comments.authtoken.models import Token
from drf_comments.request import is_form_media_type
from drf_comments.response import Response
from drf_comments.test import APITestCase
from drf_comments.views import APIView
=======
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.request import is_form_media_type
from rest_framework.response import Response
from rest_framework.test import APITestCase
from rest_framework.views import APIView
>>>>>>> e13688f0c0d32672d31ef3b9474c2a9f9dd12ae9


class PostView(APIView):
    def post(self, request):
        return Response(data=request.data, status=200)


urlpatterns = [
    path('auth', APIView.as_view(authentication_classes=(TokenAuthentication,))),
    path('post', PostView.as_view()),
]


class RequestUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        assert hasattr(request, 'user'), '`user` is not set on request'
        assert request.user.is_authenticated, '`user` is not authenticated'

        return response


class RequestPOSTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        assert isinstance(request, HttpRequest)

        # Parse body with underlying Django request
        request.body

        # Process request with DRF view
        response = self.get_response(request)

        # Ensure request.POST is set as appropriate
        if is_form_media_type(request.content_type):
            assert request.POST == {'foo': ['bar']}
        else:
            assert request.POST == {}

        return response


@override_settings(ROOT_URLCONF='tests.test_middleware')
class TestMiddleware(APITestCase):

    @override_settings(MIDDLEWARE=('tests.test_middleware.RequestUserMiddleware',))
    def test_middleware_can_access_user_when_processing_response(self):
        user = User.objects.create_user('john', 'john@example.com', 'password')
        key = 'abcd1234'
        Token.objects.create(key=key, user=user)

        self.client.get('/auth', HTTP_AUTHORIZATION='Token %s' % key)

    @override_settings(MIDDLEWARE=('tests.test_middleware.RequestPOSTMiddleware',))
    def test_middleware_can_access_request_post_when_processing_response(self):
        response = self.client.post('/post', {'foo': 'bar'})
        assert response.status_code == 200

        response = self.client.post('/post', {'foo': 'bar'}, format='json')
        assert response.status_code == 200
