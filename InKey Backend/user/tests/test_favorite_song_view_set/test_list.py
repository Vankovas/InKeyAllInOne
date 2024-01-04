from http import HTTPStatus
from django.urls import reverse
from account_management.tests.mixin.test_user_mixin import TestUserMixin
from creator.models import Album, Song
from user.models import FavoriteSong


class TestListFavoriteSongViewSet(TestUserMixin):
    def setUp(self) -> None:
        super(TestListFavoriteSongViewSet, self).setUp()
        self.album = Album.objects.create(artist=self.user_other, name="new album")
        self.songs = [
            Song.objects.create(name="song1", album=self.album),
            Song.objects.create(name="song2", album=self.album),
            Song.objects.create(name="song3", album=self.album)
        ]
        self.favorite_songs = [
            FavoriteSong.objects.create(user_id=self.user.id, song_id=self.songs[0].id),
            FavoriteSong.objects.create(user_id=self.user.id, song_id=self.songs[2].id)
        ]

    def test_list_favorite_songs_unauthenticated(self):
        response = self.client_unauthenticated.get(reverse("favorite_song-list"))
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_favorite_songs_works(self):
        response = self.client.get(reverse("favorite_song-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        all_songs = response.json()
        self.assertEqual(len(all_songs), 2)
