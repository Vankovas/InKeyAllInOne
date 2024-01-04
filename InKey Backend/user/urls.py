from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'playlists', views.PlaylistViewSet, basename='playlist')
router.register(r'rate/playlists', views.PlaylistVoteViewSet, basename='playlist_vote')
router.register(r'stream', views.StreamViewSet, basename='stream')
router.register(r'comments/song', views.CommentSongViewSet, basename='comment_song')
router.register(r'comments/album', views.CommentAlbumViewSet, basename='comment_album')
router.register(r'favorite/songs', views.FavoriteSongViewSet, basename='favorite_song')
router.register(r'favorite/albums', views.FavoriteAlbumViewSet, basename='favorite_album')
router.register(r'favorite/artists', views.FavoriteArtistViewSet, basename='favorite_artist')

urlpatterns = [
    path("", include(router.urls)),
]
