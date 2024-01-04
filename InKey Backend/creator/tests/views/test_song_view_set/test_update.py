from http import HTTPStatus
from django.urls import reverse
from account_management.tests.mixin.test_user_mixin import TestUserMixin
from creator.models import Album, Song


class TestUpdateSongView(TestUserMixin):
    def setUp(self) -> None:
        super(TestUpdateSongView, self).setUp()

        self.album = Album.objects.create(name="yes", artist=self.user)
        self.album2 = Album.objects.create(name="yes2", artist=self.user)
        self.song = Song.objects.create(name="song1", album=self.album)

        self.album_other = Album.objects.create(name="no", artist=self.user_other)
        self.song_other = Song.objects.create(name="song2", album=self.album_other)
        self.correct_data = {
            "name": "newer name",
            "album": self.album.pk,
            "data": self.get_wav_audio_for_upload()
        }

    def test_update_song_unauthenticated(self):
        response = self.client_unauthenticated.put(
            reverse("song-detail", kwargs={"pk": self.song.pk}),
            self.correct_data
        )
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.song.refresh_from_db()
        self.assertNotEqual(self.song.name, "newer name")

    def test_update_song_works(self):
        response = self.client.put(
            reverse("song-detail", kwargs={"pk": self.song.pk}),
            self.correct_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.song.refresh_from_db()
        self.assertEqual(self.song.name, "newer name")

    def test_update_song_can_change_album(self):
        response = self.client.patch(
            reverse("song-detail", kwargs={"pk": self.song.pk}),
            {
                "name": "newer name",
                "album": self.album2.pk
            }
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.song.refresh_from_db()
        self.assertEqual(self.song.name, "newer name")
        self.assertEqual(self.song.album, self.album2)

    def test_update_song_of_another_person_raises_error(self):
        response = self.client.put(
            reverse("song-detail", kwargs={"pk": self.song_other.pk}),
            {
                "name": "newer name",
                "album": self.album.pk
            }
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.song_other.refresh_from_db()
        self.assertNotEqual(self.song_other.name, "newer name")
