from django.urls import include, path

from .views import MockView

urlpatterns = [
    path('', MockView.as_view()),
    path('auth/', include('drf_comments.urls', namespace='drf_comments')),
]
