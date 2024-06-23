# [I forked this from DRF]

# [Django REST framework][docs]

[![build-status-image]][build-status]
[![coverage-status-image]][codecov]
[![pypi-version]][pypi]

**Awesome web-browsable Web APIs.**

Full documentation for the project is available at [https://www.django-rest-framework.org/][docs].

---

# Funding

REST framework is a *collaboratively funded project*. If you use
REST framework commercially we strongly encourage you to invest in its
continued development by [signing up for a paid plan][funding].

The initial aim is to provide a single full-time position on REST framework.
*Every single sign-up makes a significant impact towards making that possible.*

[![][sentry-img]][sentry-url]
[![][stream-img]][stream-url]
[![][spacinov-img]][spacinov-url]
[![][retool-img]][retool-url]
[![][bitio-img]][bitio-url]
[![][posthog-img]][posthog-url]
[![][cryptapi-img]][cryptapi-url]
[![][fezto-img]][fezto-url]
[![][svix-img]][svix-url]

Many thanks to all our [wonderful sponsors][sponsors], and in particular to our premium backers, [Sentry][sentry-url], [Stream][stream-url], [Spacinov][spacinov-url], [Retool][retool-url], [bit.io][bitio-url], [PostHog][posthog-url], [CryptAPI][cryptapi-url], [FEZTO][fezto-url], and [Svix][svix-url].

---

# Overview

Django REST framework is a powerful and flexible toolkit for building Web APIs.

Some reasons you might want to use REST framework:

* The Web browsable API is a huge usability win for your developers.
* [Authentication policies][authentication] including optional packages for [OAuth1a][oauth1-section] and [OAuth2][oauth2-section].
* [Serialization][serializers] that supports both [ORM][modelserializer-section] and [non-ORM][serializer-section] data sources.
* Customizable all the way down - just use [regular function-based views][functionview-section] if you don't need the [more][generic-views] [powerful][viewsets] [features][routers].
* [Extensive documentation][docs], and [great community support][group].

**Below**: *Screenshot from the browsable API*

![Screenshot][image]

----

# Requirements

* Python 3.8+
* Django 5.0, 4.2

We **highly recommend** and only officially support the latest patch release of
each Python and Django series.

# Installation

Install using `pip`...

    pip install drf-comments

Add `'drf_comments'` to your `INSTALLED_APPS` setting.
```python
INSTALLED_APPS = [
    ...
    'drf_comments',
]
```

# Example

Let's take a look at a quick example of using REST framework to build a simple model-backed API for accessing users and groups.

Startup up a new project like so...

    pip install django
    pip install drf-comments
    django-admin startproject example .
    ./manage.py migrate
    ./manage.py createsuperuser

Since this is a fork of django-rest-framework you do not need to install it unless this package is not up-to-date with the current django-rest-framework available

Now edit the `example/urls.py` module in your project:

```python
from django.db import models
from django.contrib.auth.models import User
from drf_comments import serializers, viewsets
from drf_comments.comments import CommentViewSet, BaseComment, comment_serializer, create_comment_serializer
from drf_comments.permissions import IsAuthenticated
from drf_comments.authentication import TokenAuthentication

# model to add comments to
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class PostComment(BaseComment):
    object = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True) # in version 0.8.2 blank=True and null=True had to be set, in 0.8.3 they are not needed

#serializer
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'content', 'created_at', 'updated_at']

#viewsets
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

class PostCommentViewSet(CommentViewSet):
    queryset = PostComment.objects.all()
    serializer_class = comment_serializer(PostComment)
    create_serializer_class = create_comment_serializer(PostComment)

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

# Routers provide a way of automatically determining the URL conf.
router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'posts/(?P<object_id>\d+)/comments', PostCommentViewSet, basename='post-comments')

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('', include(router.urls)),
]
```

We'd also like to configure a couple of settings for our API.

Add the following to your `settings.py` module:

```python
INSTALLED_APPS = [
    ...  # Make sure to include the default installed apps here.
    'drf_comments',
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'drf_comments.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ]
}
```

That's it, we're done!

    ./manage.py runserver

You can now open the API in your browser at `http://127.0.0.1:8000/`, and view your new 'users' API. If you use the `Login` control in the top right corner you'll also be able to add, create and delete users from the system.

You can also interact with the API using command line tools such as [`curl`](https://curl.haxx.se/). For example:

    $ curl -X POST http://localhost:8000/posts/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Token YOUR_AUTH_TOKEN" \
    -d '{
            "user": 1,
            "title": "First Post",
            "content": "This is the content of the first post."
        }'

And to create a comment tp that post:

    $ curl -X POST http://localhost:8000/posts/1/comments/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Token YOUR_AUTH_TOKEN" \
    -d '{
            "user": 1,
            "text": "This is a comment on the first post."
        }'

You can also use requests.py to make API calls like so:

```python
import requests

url = "http://localhost:8000/posts/"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token YOUR_AUTH_TOKEN"
}
data = {
    "user": 1,
    "title": "First Post",
    "content": "This is the content of the first post."
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)
print(response.json())
```
And:
```python
import requests

url = "http://localhost:8000/posts/1/comments/"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token YOUR_AUTH_TOKEN"
}
data = {
    "user": 1,
    "text": "This is a comment on the first post."
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)
print(response.json())

```

# Documentation & Support

Full documentation for the project is available at [https://www.django-rest-framework.org/][docs].

For questions and support, use the [REST framework discussion group][group], or `#restframework` on libera.chat IRC.

# Security

Please see the [security policy][security-policy].

[build-status-image]: https://github.com/encode/django-rest-framework/actions/workflows/main.yml/badge.svg
[build-status]: https://github.com/encode/django-rest-framework/actions/workflows/main.yml
[coverage-status-image]: https://img.shields.io/codecov/c/github/encode/django-rest-framework/master.svg
[codecov]: https://codecov.io/github/encode/django-rest-framework?branch=master
[pypi-version]: https://img.shields.io/pypi/v/djangorestframework.svg
[pypi]: https://pypi.org/project/djangorestframework/
[group]: https://groups.google.com/forum/?fromgroups#!forum/django-rest-framework

[funding]: https://fund.django-rest-framework.org/topics/funding/
[sponsors]: https://fund.django-rest-framework.org/topics/funding/#our-sponsors

[sentry-img]: https://raw.githubusercontent.com/encode/django-rest-framework/master/docs/img/premium/sentry-readme.png
[stream-img]: https://raw.githubusercontent.com/encode/django-rest-framework/master/docs/img/premium/stream-readme.png
[spacinov-img]: https://raw.githubusercontent.com/encode/django-rest-framework/master/docs/img/premium/spacinov-readme.png
[retool-img]: https://raw.githubusercontent.com/encode/django-rest-framework/master/docs/img/premium/retool-readme.png
[bitio-img]: https://raw.githubusercontent.com/encode/django-rest-framework/master/docs/img/premium/bitio-readme.png
[posthog-img]: https://raw.githubusercontent.com/encode/django-rest-framework/master/docs/img/premium/posthog-readme.png
[cryptapi-img]: https://raw.githubusercontent.com/encode/django-rest-framework/master/docs/img/premium/cryptapi-readme.png
[fezto-img]: https://raw.githubusercontent.com/encode/django-rest-framework/master/docs/img/premium/fezto-readme.png
[svix-img]: https://raw.githubusercontent.com/encode/django-rest-framework/master/docs/img/premium/svix-premium.png

[sentry-url]: https://getsentry.com/welcome/
[stream-url]: https://getstream.io/?utm_source=DjangoRESTFramework&utm_medium=Webpage_Logo_Ad&utm_content=Developer&utm_campaign=DjangoRESTFramework_Jan2022_HomePage
[spacinov-url]: https://www.spacinov.com/
[retool-url]: https://retool.com/?utm_source=djangorest&utm_medium=sponsorship
[bitio-url]: https://bit.io/jobs?utm_source=DRF&utm_medium=sponsor&utm_campaign=DRF_sponsorship
[posthog-url]: https://posthog.com?utm_source=drf&utm_medium=sponsorship&utm_campaign=open-source-sponsorship
[cryptapi-url]: https://cryptapi.io
[fezto-url]: https://www.fezto.xyz/?utm_source=DjangoRESTFramework
[svix-url]: https://www.svix.com/?utm_source=django-REST&utm_medium=sponsorship

[oauth1-section]: https://www.django-rest-framework.org/api-guide/authentication/#django-rest-framework-oauth
[oauth2-section]: https://www.django-rest-framework.org/api-guide/authentication/#django-oauth-toolkit
[serializer-section]: https://www.django-rest-framework.org/api-guide/serializers/#serializers
[modelserializer-section]: https://www.django-rest-framework.org/api-guide/serializers/#modelserializer
[functionview-section]: https://www.django-rest-framework.org/api-guide/views/#function-based-views
[generic-views]: https://www.django-rest-framework.org/api-guide/generic-views/
[viewsets]: https://www.django-rest-framework.org/api-guide/viewsets/
[routers]: https://www.django-rest-framework.org/api-guide/routers/
[serializers]: https://www.django-rest-framework.org/api-guide/serializers/
[authentication]: https://www.django-rest-framework.org/api-guide/authentication/
[image]: https://www.django-rest-framework.org/img/quickstart.png

[docs]: https://www.django-rest-framework.org/
[security-policy]: https://github.com/encode/django-rest-framework/security/policy
