import re

from django.shortcuts import render


def test_base_template_with_context():
    context = {'request': True, 'csrf_token': 'TOKEN'}
<<<<<<< HEAD
    result = render({}, 'drf_comments/base.html', context=context)
=======
    result = render({}, 'rest_framework/base.html', context=context)
>>>>>>> e13688f0c0d32672d31ef3b9474c2a9f9dd12ae9
    assert re.search(r'"csrfToken": "TOKEN"', result.content.decode())


def test_base_template_with_no_context():
    # base.html should be renderable with no context,
    # so it can be easily extended.
<<<<<<< HEAD
    result = render({}, 'drf_comments/base.html')
=======
    result = render({}, 'rest_framework/base.html')
>>>>>>> e13688f0c0d32672d31ef3b9474c2a9f9dd12ae9
    # note that this response will not include a valid CSRF token
    assert re.search(r'"csrfToken": ""', result.content.decode())
