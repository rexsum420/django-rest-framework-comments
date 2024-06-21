"""
URLConf for test suite.

We need only the docs urls for DocumentationRenderer tests.
"""
from django.urls import path

from drf_comments.compat import coreapi
from drf_comments.documentation import include_docs_urls

if coreapi:
    urlpatterns = [
        path('docs/', include_docs_urls(title='Test Suite API')),
    ]
else:
    urlpatterns = []
