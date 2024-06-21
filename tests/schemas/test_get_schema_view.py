import pytest
from django.test import TestCase, override_settings

<<<<<<< HEAD
from drf_comments import renderers
from drf_comments.schemas import coreapi, get_schema_view, openapi
=======
from rest_framework import renderers
from rest_framework.schemas import coreapi, get_schema_view, openapi
>>>>>>> e13688f0c0d32672d31ef3b9474c2a9f9dd12ae9


class GetSchemaViewTests(TestCase):
    """For the get_schema_view() helper."""
    def test_openapi(self):
        schema_view = get_schema_view(title="With OpenAPI")
        assert isinstance(schema_view.initkwargs['schema_generator'], openapi.SchemaGenerator)
        assert renderers.OpenAPIRenderer in schema_view.cls().renderer_classes

    @pytest.mark.skipif(not coreapi.coreapi, reason='coreapi is not installed')
    def test_coreapi(self):
<<<<<<< HEAD
        with override_settings(REST_FRAMEWORK={'DEFAULT_SCHEMA_CLASS': 'drf_comments.schemas.AutoSchema'}):
=======
        with override_settings(REST_FRAMEWORK={'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema'}):
>>>>>>> e13688f0c0d32672d31ef3b9474c2a9f9dd12ae9
            schema_view = get_schema_view(title="With CoreAPI")
            assert isinstance(schema_view.initkwargs['schema_generator'], coreapi.SchemaGenerator)
            assert renderers.CoreAPIOpenAPIRenderer in schema_view.cls().renderer_classes
