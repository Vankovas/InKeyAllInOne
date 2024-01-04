from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'albums', views.AlbumViewSet, basename='album')
router.register(r'rate/albums', views.AlbumVoteViewSet, basename='album_vote')
router.register(r'songs', views.SongViewSet, basename='song')
router.register(r'rate/songs', views.SongVoteViewSet, basename='song_vote')

urlpatterns = [
    path("", include(router.urls)),
]
