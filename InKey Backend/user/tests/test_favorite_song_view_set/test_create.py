from http import HTTPStatus
from django.urls import reverse
from account_management.tests.mixin.test_user_mixin import TestUserMixin
from creator.models import Album, Song
from user.models import FavoriteSong


class TestCreateFavoriteSongView(TestUserMixin):
    def setUp(self) -> None:
        super(TestCreateFavoriteSongView, self).setUp()
        self.album = Album.objects.create(artist=self.user, name="new album")
        self.song = Song.objects.create(name="new song", album=self.album, data=self.get_wav_audio_for_upload())

        self.other_album = Album.objects.create(artist=self.user_other, name='other album')
        self.other_song = Song.objects.create(name="other song", album=self.other_album,
                                              data=self.get_wav_audio_for_upload())

    def test_add_to_favorite_works(self):
        data = {
            'song_id': self.other_song.id
        }
        response = self.client.post(reverse("favorite_song-list"), data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_add_to_favorite_twice_delete(self):
        data = {
            'song_id': self.other_song.id
        }
        self.client.post(reverse("favorite_song-list"), data)
        print(f'Song is added to database: {FavoriteSong.objects.all()}')
        response = self.client.post(reverse("favorite_song-list"), data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        print(f'Song is removed from database: {FavoriteSong.objects.all()}')

    def test_add_to_favorite_no_such_song(self):
        data = {
            'song_id': self.other_song.id+1
        }
        response = self.client.post(reverse("favorite_song-list"), data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_add_favorite_song_unauthenticated(self):
        data = {
            'song_id': self.other_song.id
        }
        response = self.client_unauthenticated.post(reverse("favorite_song-list"), data)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_you_cannot_like_your_own_song(self):
        data = {
            'song_id': self.song.id
        }
        response = self.client.post(reverse("favorite_song-list"), data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)