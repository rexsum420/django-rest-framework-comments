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
from drf_comments.authtoken.views import ObtainAuthToken

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
    path('auth/', ObtainAuthToken.as_view(), name='Auth')
    path('', include(router.urls)),
]
```

We'd also like to configure a couple of settings for our API.

Add the following to your `settings.py` module:

```python
INSTALLED_APPS = [
    ...  # Make sure to include the default installed apps here.
    'drf_comments',
    'drf_comments.authtoken',
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'drf_comments.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ]
}
```
After this you will need to update the database

```bash
    ./manage.py makemigrations
    ./manage.py migrate
``` 

That's it, we're done!

    ./manage.py runserver

You can now open the API in your browser at `http://127.0.0.1:8000/`, and view your new 'post' API. If you use the `Login` control in the top right corner you'll also be able to add, create and delete users from the system.

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
            "text": "This is a comment on the first post.",
            "object": 1,
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
    "text": "This is a comment on the first post.",
    "object": 1,
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)
print(response.json())

```
