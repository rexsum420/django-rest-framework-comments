from django.test import TestCase

<<<<<<< HEAD
from drf_comments import serializers, status
from drf_comments.decorators import api_view
from drf_comments.exceptions import ValidationError
from drf_comments.response import Response
from drf_comments.settings import api_settings
from drf_comments.test import APIRequestFactory
from drf_comments.views import APIView
=======
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView
>>>>>>> e13688f0c0d32672d31ef3b9474c2a9f9dd12ae9

factory = APIRequestFactory()


class ExampleSerializer(serializers.Serializer):
    char = serializers.CharField()
    integer = serializers.IntegerField()


class ErrorView(APIView):
    def get(self, request, *args, **kwargs):
        ExampleSerializer(data={}).is_valid(raise_exception=True)


@api_view(['GET'])
def error_view(request):
    ExampleSerializer(data={}).is_valid(raise_exception=True)


class TestValidationErrorWithFullDetails(TestCase):
    def setUp(self):
        self.DEFAULT_HANDLER = api_settings.EXCEPTION_HANDLER

        def exception_handler(exc, request):
            data = exc.get_full_details()
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        api_settings.EXCEPTION_HANDLER = exception_handler

        self.expected_response_data = {
            'char': [{
                'message': 'This field is required.',
                'code': 'required',
            }],
            'integer': [{
                'message': 'This field is required.',
                'code': 'required'
            }],
        }

    def tearDown(self):
        api_settings.EXCEPTION_HANDLER = self.DEFAULT_HANDLER

    def test_class_based_view_exception_handler(self):
        view = ErrorView.as_view()

        request = factory.get('/', content_type='application/json')
        response = view(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == self.expected_response_data

    def test_function_based_view_exception_handler(self):
        view = error_view

        request = factory.get('/', content_type='application/json')
        response = view(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == self.expected_response_data


class TestValidationErrorWithCodes(TestCase):
    def setUp(self):
        self.DEFAULT_HANDLER = api_settings.EXCEPTION_HANDLER

        def exception_handler(exc, request):
            data = exc.get_codes()
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        api_settings.EXCEPTION_HANDLER = exception_handler

        self.expected_response_data = {
            'char': ['required'],
            'integer': ['required'],
        }

    def tearDown(self):
        api_settings.EXCEPTION_HANDLER = self.DEFAULT_HANDLER

    def test_class_based_view_exception_handler(self):
        view = ErrorView.as_view()

        request = factory.get('/', content_type='application/json')
        response = view(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == self.expected_response_data

    def test_function_based_view_exception_handler(self):
        view = error_view

        request = factory.get('/', content_type='application/json')
        response = view(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == self.expected_response_data


class TestValidationErrorConvertsTuplesToLists(TestCase):
    def test_validation_error_details(self):
        error = ValidationError(detail=('message1', 'message2'))
        assert isinstance(error.detail, list)
        assert len(error.detail) == 2
        assert str(error.detail[0]) == 'message1'
        assert str(error.detail[1]) == 'message2'
