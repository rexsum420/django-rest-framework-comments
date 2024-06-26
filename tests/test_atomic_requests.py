import unittest

from django.db import connection, connections, transaction
from django.http import Http404
from django.test import TestCase, TransactionTestCase, override_settings
from django.urls import path

<<<<<<< HEAD
from drf_comments import status
from drf_comments.exceptions import APIException
from drf_comments.response import Response
from drf_comments.test import APIRequestFactory
from drf_comments.views import APIView
=======
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView
>>>>>>> e13688f0c0d32672d31ef3b9474c2a9f9dd12ae9
from tests.models import BasicModel

factory = APIRequestFactory()


class BasicView(APIView):
    def post(self, request, *args, **kwargs):
        BasicModel.objects.create()
        return Response({'method': 'GET'})


class ErrorView(APIView):
    def post(self, request, *args, **kwargs):
        BasicModel.objects.create()
        raise Exception


class APIExceptionView(APIView):
    def post(self, request, *args, **kwargs):
        BasicModel.objects.create()
        raise APIException


class NonAtomicAPIExceptionView(APIView):
    @transaction.non_atomic_requests
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        BasicModel.objects.all()
        raise Http404


urlpatterns = (
    path('', NonAtomicAPIExceptionView.as_view()),
)


@unittest.skipUnless(
    connection.features.uses_savepoints,
    "'atomic' requires transactions and savepoints."
)
class DBTransactionTests(TestCase):
    def setUp(self):
        self.view = BasicView.as_view()
        connections.databases['default']['ATOMIC_REQUESTS'] = True

    def tearDown(self):
        connections.databases['default']['ATOMIC_REQUESTS'] = False

    def test_no_exception_commit_transaction(self):
        request = factory.post('/')

        with self.assertNumQueries(1):
            response = self.view(request)
        assert not transaction.get_rollback()
        assert response.status_code == status.HTTP_200_OK
        assert BasicModel.objects.count() == 1


@unittest.skipUnless(
    connection.features.uses_savepoints,
    "'atomic' requires transactions and savepoints."
)
class DBTransactionErrorTests(TestCase):
    def setUp(self):
        self.view = ErrorView.as_view()
        connections.databases['default']['ATOMIC_REQUESTS'] = True

    def tearDown(self):
        connections.databases['default']['ATOMIC_REQUESTS'] = False

    def test_generic_exception_delegate_transaction_management(self):
        """
        Transaction is eventually managed by outer-most transaction atomic
        block. DRF do not try to interfere here.

        We let django deal with the transaction when it will catch the Exception.
        """
        request = factory.post('/')
        with self.assertNumQueries(3):
            # 1 - begin savepoint
            # 2 - insert
            # 3 - release savepoint
            with transaction.atomic():
                self.assertRaises(Exception, self.view, request)
                assert not transaction.get_rollback()
        assert BasicModel.objects.count() == 1


@unittest.skipUnless(
    connection.features.uses_savepoints,
    "'atomic' requires transactions and savepoints."
)
class DBTransactionAPIExceptionTests(TestCase):
    def setUp(self):
        self.view = APIExceptionView.as_view()
        connections.databases['default']['ATOMIC_REQUESTS'] = True

    def tearDown(self):
        connections.databases['default']['ATOMIC_REQUESTS'] = False

    def test_api_exception_rollback_transaction(self):
        """
        Transaction is rollbacked by our transaction atomic block.
        """
        request = factory.post('/')
        num_queries = 4 if connection.features.can_release_savepoints else 3
        with self.assertNumQueries(num_queries):
            # 1 - begin savepoint
            # 2 - insert
            # 3 - rollback savepoint
            # 4 - release savepoint
            with transaction.atomic():
                response = self.view(request)
                assert transaction.get_rollback()
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert BasicModel.objects.count() == 0


@unittest.skipUnless(
    connection.features.uses_savepoints,
    "'atomic' requires transactions and savepoints."
)
class MultiDBTransactionAPIExceptionTests(TestCase):
    databases = '__all__'

    def setUp(self):
        self.view = APIExceptionView.as_view()
        connections.databases['default']['ATOMIC_REQUESTS'] = True
        connections.databases['secondary']['ATOMIC_REQUESTS'] = True

    def tearDown(self):
        connections.databases['default']['ATOMIC_REQUESTS'] = False
        connections.databases['secondary']['ATOMIC_REQUESTS'] = False

    def test_api_exception_rollback_transaction(self):
        """
        Transaction is rollbacked by our transaction atomic block.
        """
        request = factory.post('/')
        num_queries = 4 if connection.features.can_release_savepoints else 3
        with self.assertNumQueries(num_queries):
            # 1 - begin savepoint
            # 2 - insert
            # 3 - rollback savepoint
            # 4 - release savepoint
            with transaction.atomic(), transaction.atomic(using='secondary'):
                response = self.view(request)
                assert transaction.get_rollback()
                assert transaction.get_rollback(using='secondary')
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert BasicModel.objects.count() == 0


@unittest.skipUnless(
    connection.features.uses_savepoints,
    "'atomic' requires transactions and savepoints."
)
@override_settings(ROOT_URLCONF='tests.test_atomic_requests')
class NonAtomicDBTransactionAPIExceptionTests(TransactionTestCase):
    def setUp(self):
        connections.databases['default']['ATOMIC_REQUESTS'] = True

    def tearDown(self):
        connections.databases['default']['ATOMIC_REQUESTS'] = False

    def test_api_exception_rollback_transaction_non_atomic_view(self):
        response = self.client.get('/')

        # without checking connection.in_atomic_block view raises 500
        # due attempt to rollback without transaction
        assert response.status_code == status.HTTP_404_NOT_FOUND
