from http import HTTPStatus
from django.urls import reverse
from account_management.tests.mixin.test_user_mixin import TestUserMixin
from creator.models import Album, Song


class TestRetrieveAndListSongView(TestUserMixin):
    def setUp(self) -> None:
        super(TestRetrieveAndListSongView, self).setUp()
        album = Album.objects.create(name="yes1", artist=self.user)
        album_other = Album.objects.create(name="yes2", artist=self.user_other)
        private_album = Album.objects.create(name="private album", artist=self.user, is_private=True)
        self.full_object = {
            "name": "name4",
            "album": private_album,
            "views": 100,
            "description": "Yes",
            "data": self.get_wav_audio_for_upload()
        }
        self.songs = [
            Song.objects.create(name="name1", album=album),
            Song.objects.create(name="name2", album=album),
            Song.objects.create(name="name3", album=album),
            Song.objects.create(**self.full_object),
        ]
        self.songs_other = [
            Song.objects.create(name="other1", album=album_other),
            Song.objects.create(name="other2", album=album_other),
        ]
    
    def test_list_songs_unauthenticated(self):
        response = self.client_unauthenticated.get(reverse("song-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        
    def test_retrieve_song_unauthenticated(self):
        response = self.client_unauthenticated.get(reverse("song-detail", kwargs={"pk": self.songs[0].pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_list_songs_works(self):
        response = self.client.get(reverse("song-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        all_songs = response.json()
        self.assertEqual(len(all_songs), 6)

    def test_list_songs_other_works(self):
        response = self.client_other.get(reverse("song-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        all_songs = response.json()
        self.assertEqual(len(all_songs), 5)

    def test_retrieve_song_works(self):
        response = self.client.get(reverse("song-detail", kwargs={"pk": self.songs[0].pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        song = response.json()
        self.assertEqual(song["name"], self.songs[0].name)

    def test_retrieve_song_all_fields_custom_works_and_also_updates_views(self):
        response = self.client.get(reverse("song-detail", kwargs={"pk": self.songs[3].pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        song = response.json()
        self.assertEqual(song["name"], self.full_object["name"])
        self.assertEqual(song["album"], self.full_object["album"].id)
        self.assertEqual(song["views"], self.full_object["views"] + 1)
        self.assertEqual(song["description"], self.full_object["description"])
        self.assertIn(self.full_object["data"].name[0:-4], song["data"])

    def test_retrieve_song_in_private_album_works_if_album_belongs_to_user(self):
        response = self.client.get(reverse("song-detail", kwargs={"pk": self.songs[3].pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        song = response.json()
        self.assertEqual(song["name"], self.songs[3].name)

    def test_retrieve_song_in_private_album_doesnt_work_if_album_doesnt_belong_to_user(self):
        response = self.client_other.get(reverse("song-detail", kwargs={"pk": self.songs[3].pk}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_retreve_song_returns_artist_name(self):
        self.user.firstname = "This is my name"
        self.user.save()
        response = self.client.get(reverse("song-detail", kwargs={"pk": self.songs[0].pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        song = response.json()
        self.assertEqual(song["artist_name"], "This is my name")
        self.assertEqual(song["artist_name"], self.user.firstname)
