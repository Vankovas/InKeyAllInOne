import django_filters
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from core.abstract_views import AbstractViewsIncrementRetrieveViewSet, AbstractAuthenticatedView
from creator.models import Song, Album
from creator.permissions import BelongsToArtistPermission
from creator.views import AbstractVoteViewSet
from user.models import Playlist, FavoriteSong, FavoriteAlbum, FavoriteArtist, CommentSong, CommentAlbum, Stream, \
    PlaylistVote
from account_management.serializers import UserSerializer
from account_management.models import User
from rest_framework.response import Response
from rest_framework import status, exceptions, mixins, viewsets
from django.db import IntegrityError
from creator.serializers import AlbumSerializer, SongSerializer
from user.permissions import BelongsToUserPermission
from user.serializers import PlaylistSerializer, CommentSongSerializer, CommentAlbumSerializer, StreamSerializer, \
    PlaylistVoteSerializer
from rest_framework import filters


class StreamViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer
    lookup_field = "artist__id"

    def get_permissions(self):
        if self.action in ["destroy"]:
            self.permission_classes = [IsAuthenticated, BelongsToArtistPermission]
        if self.action in ["create"]:
            self.permission_classes = [IsAuthenticated]
        if self.action in ["list", "retrieve"]:
            self.permission_classes = []
        return super(StreamViewSet, self).get_permissions()


class AbstractCommentViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['comment__user__id', 'comment__date_of_creation', 'comment__last_edited']
    ordering_fields = '__all__'

    def get_permissions(self):
        if self.action in ["create"]:
            self.permission_classes = [IsAuthenticated]
        if self.action in ["retrieve"]:
            self.permission_classes = []
        return super(AbstractCommentViewSet, self).get_permissions()


class CommentSongViewSet(AbstractCommentViewSet):
    serializer_class = CommentSongSerializer

    def get_queryset(self):
        userpk = self.request.user if self.request.user.is_authenticated else -1
        qs = CommentSong.objects.filter(Q(song__album__artist=userpk) | Q(song__album__is_private=False))
        song = self.request.GET.get('song', None)
        if song:
            return qs.filter(song=song)
        return qs


class CommentAlbumViewSet(AbstractCommentViewSet):
    serializer_class = CommentAlbumSerializer

    def get_queryset(self):
        userpk = self.request.user if self.request.user.is_authenticated else -1
        qs = CommentAlbum.objects.filter(Q(album__artist=userpk) | Q(album__is_private=False))
        album = self.request.GET.get('album', None)
        if album:
            return qs.filter(album=album)
        return qs


class PlaylistViewSet(AbstractViewsIncrementRetrieveViewSet):
    serializer_class = PlaylistSerializer
    queryset = Playlist.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = '__all__'
    filterset_fields = ['user']

    def get_permissions(self):
        if self.action in ["destroy", "update", "update_partial", "partial_update"]:
            self.permission_classes = [IsAuthenticated, BelongsToUserPermission]
        if self.action in ["create"]:
            self.permission_classes = [IsAuthenticated]
        if self.action in ["list", "retrieve"]:
            self.permission_classes = []
        return super(PlaylistViewSet, self).get_permissions()


class PlaylistVoteViewSet(AbstractVoteViewSet):
    serializer_class = PlaylistVoteSerializer
    queryset = PlaylistVote.objects.all()
    filterset_fields = ['playlist__id']


class FavoriteSongViewSet(AbstractAuthenticatedView):
    serializer_class = SongSerializer

    def get_permissions(self):
        if self.action in ["create", "list"]:
            self.permission_classes = [IsAuthenticated]
        return super(FavoriteSongViewSet, self).get_permissions()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Song.objects.filter(in_favorites__user_id=self.request.user)
        else:
            raise exceptions.AuthenticationFailed('No such user')

    def create(self, request, *args, **kwargs):
        try:
            song_id = request.data.get('song_id')
            user_id = self.request.user.id
            song_creator = User.objects.get(albums__songs=song_id).id
            # id user tries to like their own song return 400
            if user_id == song_creator:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            try:
                # if the user has liked the song - remove it from favorite
                FavoriteSong.objects.get(Q(song_id=song_id), Q(user_id=user_id)).delete()
            except FavoriteSong.DoesNotExist:
                # else add it to favorite
                FavoriteSong.objects.create(song_id=song_id, user_id=user_id)
            return Response(status=status.HTTP_201_CREATED)
        except (IntegrityError, User.DoesNotExist):
            return Response(status=status.HTTP_400_BAD_REQUEST)


class FavoriteAlbumViewSet(AbstractAuthenticatedView):
    serializer_class = AlbumSerializer

    def get_permissions(self):
        if self.action in ["create", "list"]:
            self.permission_classes = [IsAuthenticated]
        return super(FavoriteAlbumViewSet, self).get_permissions()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Album.objects.filter(in_favorites__user_id=self.request.user.id)
        else:
            raise exceptions.AuthenticationFailed('No such user')

    def create(self, request, *args, **kwargs):
        try:
            album_id = request.data.get('album_id')
            user_id = self.request.user.id
            album_creator = User.objects.get(albums=album_id).id
            # if user tries to like their own album return 400
            if user_id == album_creator:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            try:
                FavoriteAlbum.objects.get(Q(album_id=album_id), Q(user_id=user_id)).delete()
            except FavoriteAlbum.DoesNotExist:
                FavoriteAlbum.objects.create(album_id=album_id, user_id=user_id)
            return Response(status=status.HTTP_201_CREATED)
        except (IntegrityError, User.DoesNotExist):
            return Response(status=status.HTTP_400_BAD_REQUEST)


class FavoriteArtistViewSet(AbstractAuthenticatedView):
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ["create", "list"]:
            self.permission_classes = [IsAuthenticated]
        return super(FavoriteArtistViewSet, self).get_permissions()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return User.objects.filter(in_favorites__user_id=self.request.user.id)
        else:
            raise exceptions.AuthenticationFailed('No such user')

    def create(self, request, *args, **kwargs):
        try:
            artist_id = int(request.data.get('artist_id'))
            if len(User.objects.filter(id=artist_id)) == 0:
                return Response(data={"user": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            if artist_id == self.request.user.id:
                # user cannot add himself/herself to favorite
                return Response(data={"user": "You cannot like yourself."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    FavoriteArtist.objects.get(Q(artist_id=artist_id), Q(user_id=self.request.user.id)).delete()
                except FavoriteArtist.DoesNotExist:
                    FavoriteArtist.objects.create(artist_id=artist_id, user_id=self.request.user.id)
                return Response(status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
