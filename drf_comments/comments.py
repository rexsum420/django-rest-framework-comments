from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from rest_framework import serializers, viewsets

# Base Comment Model
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.user}'

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


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'created_at', 'updated_at', 'replies', 'parent']

    def get_replies(self, obj):
        if obj.is_parent:
            return self.__class__(obj.children(), many=True).data
        return None

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'parent']

    def validate(self, data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            data['user'] = request.user
        data['parent'] = data.get('parent', None)
        return data

def create_comment_serializer_for(amodel):
    class DynamicCommentSerializer(CommentSerializer):
        class Meta(CommentSerializer.Meta):
            model = create_comment_model_for(amodel)

    return DynamicCommentSerializer

def create_comment_create_serializer_for(amodel):
    class DynamicCommentCreateSerializer(CommentCreateSerializer):
        class Meta(CommentCreateSerializer.Meta):
            model = create_comment_model_for(amodel)

    return DynamicCommentCreateSerializer

class CommentViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return self.model.objects.all()
    
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH', 'PUT']:
            return self.create_serializer_class
        return self.serializer_class