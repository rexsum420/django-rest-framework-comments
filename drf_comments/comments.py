from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from rest_framework import serializers, viewsets, generics
from rest_framework.permissions import IsAuthenticated

# Base Comment Model
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    text = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.user} on {self.content_object}'

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        return self.parent is None


# Function to create a Comment Model dynamically
def create_comment_model_for(model):
    class Meta:
        proxy = True
        verbose_name = f'{model.__name__} Comment'
        verbose_name_plural = f'{model.__name__} Comments'

    attrs = {
        '__module__': model.__module__,
        'Meta': Meta,
    }

    return type(f'{model.__name__}Comment', (Comment,), attrs)


# Function to create a Comment Serializer dynamically
def create_comment_serializer_for(amodel):
    class DynamicCommentSerializer(serializers.ModelSerializer):
        replies = serializers.SerializerMethodField()

        class Meta:
            model = create_comment_model_for(amodel)
            fields = ['id', 'user', 'text', 'created_at', 'updated_at', 'replies', 'parent']

        def get_replies(self, obj):
            if obj.is_parent:
                return self.__class__(obj.children(), many=True).data
            return None

    return DynamicCommentSerializer


def create_comment_create_serializer_for(amodel):
    class DynamicCommentCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = create_comment_model_for(amodel)
            fields = ['id', 'user', 'text', 'parent', 'content_type', 'object_id']

    return DynamicCommentCreateSerializer


# Function to create a Comment ViewSet dynamically
def create_comment_viewset_for(amodel):
    class DynamicCommentViewSet(viewsets.ModelViewSet):
        serializer_class = create_comment_serializer_for(amodel)
        permission_classes = [IsAuthenticated]

        def get_queryset(self):
            content_type = ContentType.objects.get_for_model(amodel)
            return create_comment_model_for(amodel).objects.filter(content_type=content_type, object_id=self.kwargs['object_id'])

        def get_serializer_class(self):
            if self.action in ['create', 'update', 'partial_update']:
                return create_comment_create_serializer_for(amodel)
            return self.serializer_class

        def perform_create(self, serializer):
            content_type = ContentType.objects.get_for_model(amodel)
            serializer.save(user=self.request.user, content_type=content_type, object_id=self.kwargs['object_id'])

    return DynamicCommentViewSet


# # Example usage for Post model
# PostComment = create_comment_model_for(Post)
# PostCommentSerializer = create_comment_serializer_for(Post)
# PostCommentCreateSerializer = create_comment_create_serializer_for(Post)
# PostCommentViewSet = create_comment_viewset_for(Post)

# # URLs
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'posts/(?P<object_id>\d+)/comments', PostCommentViewSet, basename='post-comments')

# urlpatterns = [
#     path('', include(router.urls)),
# ]
