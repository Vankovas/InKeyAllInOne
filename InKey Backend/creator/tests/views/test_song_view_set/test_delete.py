from http import HTTPStatus
from django.urls import reverse
from account_management.tests.mixin.test_user_mixin import TestUserMixin
from creator.models import Album, Song


class TestDeleteSongView(TestUserMixin):
    def setUp(self) -> None:
        super(TestDeleteSongView, self).setUp()
        self.album = Album.objects.create(name="yes1", artist=self.user)
        self.song = Song.objects.create(name="song1", album=self.album)

        self.album_other = Album.objects.create(name="yes2", artist=self.user_other)
        self.song_other = Song.objects.create(name="song2", album=self.album_other)

    def test_delete_song_unauthenticated(self):
        response = self.client_unauthenticated.delete(
            reverse("song-detail", kwargs={"pk": self.song.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(Song.objects.filter(album=self.album).count(), 1)

    def test_delete_song_works(self):
        response = self.client.delete(
            reverse("song-detail", kwargs={"pk": self.song.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Song.objects.filter(album=self.album).count(), 0)

    def test_delete_song_of_another_person_raises_error(self):
        response = self.client.delete(
            reverse("song-detail", kwargs={"pk": self.song_other.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Song.objects.filter(album=self.album_other).count(), 1)
