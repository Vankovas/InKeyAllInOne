from django.db.models import Q
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
import django_filters.rest_framework
from core.abstract_views import AbstractViewsIncrementRetrieveViewSet, AbstractAuthenticatedView
from creator.models import Album, Song, SongVote, AlbumVote
from creator.permissions import SongBelongsToUserPermission
from creator.serializers import AlbumSerializer, SongSerializer, SongVoteSerializer, AlbumVoteSerializer
from rest_framework import filters


class AlbumViewSet(AbstractViewsIncrementRetrieveViewSet, AbstractAuthenticatedView):
    serializer_class = AlbumSerializer
    queryset = Album.objects.all()
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter
    ]
    filterset_fields = ['artist__id']
    ordering_fields = '__all__'
    search_fields = ['name']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            userpk = self.request.user
        else:
            userpk = -1
        return Album.objects.filter(Q(artist=userpk) | Q(is_private=False))


class SongViewSet(AbstractViewsIncrementRetrieveViewSet):
    serializer_class = SongSerializer
    queryset = Song.objects.all()
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter
    ]
    filterset_fields = ['name', 'album__id', 'album__artist__id']
    ordering_fields = '__all__'
    search_fields = ['name']

    def get_permissions(self):
        if self.action in ["update", "destroy", "update_partial", "partial_update", "create"]:
            self.permission_classes = [IsAuthenticated, SongBelongsToUserPermission]
        if self.action in ["list", "retrieve"]:
            self.permission_classes = []
        return super(SongViewSet, self).get_permissions()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            userpk = self.request.user
        else:
            userpk = -1
        return Song.objects.filter(Q(album__artist=userpk) | Q(album__is_private=False))


class AbstractVoteViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            userpk = self.request.user
        else:
            userpk = -1
        return self.queryset.filter(user=userpk)


class SongVoteViewSet(AbstractVoteViewSet):
    serializer_class = SongVoteSerializer
    queryset = SongVote.objects.all()
    filterset_fields = ['song__id']


class AlbumVoteViewSet(AbstractVoteViewSet):
    serializer_class = AlbumVoteSerializer
    queryset = AlbumVote.objects.all()
    filterset_fields = ['album__id']
