from drf_comments import authentication, renderers
from drf_comments.permissions import BasePermission
from drf_comments.response import Response
from drf_comments.views import APIView
from drf_comments.viewsets import ModelViewSet

from ..models import BasicModelWithUsers
from .serializers import BasicSerializer


class OrganizationPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or (request.user == obj.owner.organization_user.user)


class MockView(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    renderer_classes = (renderers.BrowsableAPIRenderer, renderers.JSONRenderer)

    def get(self, request):
        return Response({'a': 1, 'b': 2, 'c': 3})


class BasicModelWithUsersViewSet(ModelViewSet):
    queryset = BasicModelWithUsers.objects.all()
    serializer_class = BasicSerializer
    permission_classes = [OrganizationPermissions]
    # permission_classes = [IsAuthenticated, OrganizationPermissions]
    renderer_classes = (renderers.BrowsableAPIRenderer, renderers.JSONRenderer)

    def get_queryset(self):
        qs = super().get_queryset().filter(users=self.request.user)
        return qs
