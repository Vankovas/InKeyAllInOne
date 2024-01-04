from http import HTTPStatus
from django.urls import reverse
from account_management.tests.mixin.test_user_mixin import TestUserMixin
from creator.models import Album


class TestCreateSongView(TestUserMixin):
    def setUp(self) -> None:
        super(TestCreateSongView, self).setUp()
        self.album = Album.objects.create(artist=self.user, name="new album")
        self.album_other = Album.objects.create(artist=self.user_other, name="inaccessible album")
        self.correct_data = {
            "name": "new song",
            "album": self.album.pk,
            "data": self.get_wav_audio_for_upload()
        }
        self.full_object = {
            "name": "full_song",
            "album": self.album.pk,
            "views": 100,
            "description": "Yes",
            "data": self.get_wav_audio_for_upload(),
        }

    def test_create_song(self):
        response = self.client.post(
            reverse("song-list"),
            self.correct_data
        )
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        response_json = response.json()
        self.assertEqual(response_json["name"], "new song")

    def test_create_song_without_name_raises_error(self):
        self.correct_data.pop("name")
        response = self.client.post(reverse("song-list"), self.correct_data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        print(response.json())

    def test_create_song_without_album_raises_error(self):
        self.correct_data.pop("album")
        response = self.client.post(reverse("song-list"), self.correct_data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json()["album"][0], "This field is required.")

    def test_create_song_without_data_raises_error(self):
        self.correct_data.pop("data")
        response = self.client.post(reverse("song-list"), self.correct_data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json()["data"][0], "No file was submitted.")

    def test_create_song_with_nonexisting_pk_user_album_raises_error(self):
        self.correct_data["album"] = self.album_other.pk+1
        response = self.client.post(reverse("song-list"), self.correct_data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json()["album"][0], "This field is required.")

    def test_create_song_unauthenticated(self):
        response = self.client_unauthenticated.post(reverse("song-list"), self.correct_data)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_create_song_with_another_user_album_raises_error(self):
        self.correct_data["album"] = self.album_other.pk
        response = self.client.post(reverse("song-list"), self.correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_create_song_with_all_fields(self):
        response = self.client.post(reverse("song-list"), self.full_object)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        song = response.json()
        self.assertEqual(song["name"], self.full_object["name"])
        self.assertEqual(song["album"], self.full_object["album"])
        self.assertNotEqual(song["views"], self.full_object["views"])
        self.assertEqual(song["views"], 0)
        self.assertEqual(song["description"], self.full_object["description"])
        self.assertIn(self.full_object["data"].name[:-4], song["data"])
