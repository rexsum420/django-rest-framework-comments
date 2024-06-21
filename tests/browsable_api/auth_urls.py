from django.urls import include, path

from .views import MockView

urlpatterns = [
    path('', MockView.as_view()),
<<<<<<< HEAD
    path('auth/', include('drf_comments.urls', namespace='drf_comments')),
=======
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
>>>>>>> e13688f0c0d32672d31ef3b9474c2a9f9dd12ae9
]
