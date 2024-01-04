from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from creator.permissions import BelongsToArtistPermission


class AbstractViewsIncrementRetrieveViewSet(ModelViewSet):
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views = instance.views + 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AbstractAuthenticatedView(ModelViewSet):
    def get_permissions(self):
        if self.action in ["update", "destroy", "update_partial", "partial_update"]:
            self.permission_classes = [IsAuthenticated, BelongsToArtistPermission]
        if self.action in ["create"]:
            self.permission_classes = [IsAuthenticated]
        if self.action in ["list", "retrieve"]:
            self.permission_classes = []
        return super(AbstractAuthenticatedView, self).get_permissions()