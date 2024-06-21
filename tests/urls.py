"""
URLConf for test suite.

We need only the docs urls for DocumentationRenderer tests.
"""
from django.urls import path

<<<<<<< HEAD
from drf_comments.compat import coreapi
from drf_comments.documentation import include_docs_urls
=======
from rest_framework.compat import coreapi
from rest_framework.documentation import include_docs_urls
>>>>>>> e13688f0c0d32672d31ef3b9474c2a9f9dd12ae9

if coreapi:
    urlpatterns = [
        path('docs/', include_docs_urls(title='Test Suite API')),
    ]
else:
    urlpatterns = []
