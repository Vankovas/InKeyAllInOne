from rest_framework import viewsets, generics
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from account_management.permissions import IsUserPermission
from account_management.serializers import MyTokenObtainPairSerializer, UserSerializer
from rest_framework import filters
User = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = '__all__'
    ordering = ['id']
    search_fields = ['firstname']

    def get_permissions(self):
        if self.action in ("update", "destroy", "partial_update"):
            self.permission_classes = [IsAuthenticated, IsUserPermission]
        elif self.action in ("list", "create", "retrieve"):
            self.permission_classes = []
        return super(UserViewSet, self).get_permissions()


class UserFromTokenView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsUserPermission]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

