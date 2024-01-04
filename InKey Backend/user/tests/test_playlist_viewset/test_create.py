from django.urls import reverse

from account_management.tests.mixin.test_user_mixin import TestUserMixin
from creator.models import Album, Song
from user.models import PlaylistTrack, Playlist


class TestPlaylistCreateViewSet(TestUserMixin):
    def setUp(self) -> None:
        super(TestPlaylistCreateViewSet, self).setUp()
        self.album = Album.objects.create(artist=self.user_other, name="new album")
        self.songs = [
            Song.objects.create(name="song1", album=self.album),
            Song.objects.create(name="song2", album=self.album),
            Song.objects.create(name="song3", album=self.album)
        ]

    def test_create_works_correctly(self):
        data = {
            "name": "new playlist",
            "description": "custom description",
        }
        self.assertEqual(Playlist.objects.count(), 0)
        response = self.client.post(reverse('playlist-list'), data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Playlist.objects.count(), 1)
        self.assertEqual(Playlist.objects.first().name, "new playlist")
        self.assertEqual(Playlist.objects.first().user, self.user)
        self.assertEqual(Playlist.objects.first().description, "custom description")

    def test_create_works_wih_name_only_correctly(self):
        data = {
            "name": "new playlist",
        }
        self.assertEqual(Playlist.objects.count(), 0)
        response = self.client.post(reverse('playlist-list'), data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Playlist.objects.count(), 1)
        self.assertEqual(Playlist.objects.first().name, "new playlist")
        self.assertEqual(Playlist.objects.first().user, self.user)

    def test_create_playlist_with_songs(self):
        data = {
            "name": "new playlist",
            "add_songs": [self.songs[0].id, self.songs[1].id],
            "description": "custom description",
        }
        self.assertEqual(Playlist.objects.count(), 0)
        self.assertEqual(PlaylistTrack.objects.count(), 0)
        response = self.client.post(reverse('playlist-list'), data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Playlist.objects.count(), 1)
        playlist = Playlist.objects.first()
        self.assertEqual(playlist.name, "new playlist")
        self.assertEqual(playlist.user, self.user)
        self.assertEqual(playlist.description, "custom description")
        self.assertEqual(PlaylistTrack.objects.count(), 2)
        self.assertEqual(len(PlaylistTrack.objects.filter(song=self.songs[0].id)), 1)
        self.assertEqual(len(PlaylistTrack.objects.filter(song=self.songs[1].id)), 1)
        self.assertEqual(len(PlaylistTrack.objects.filter(song=self.songs[2].id)), 0)

    def test_create_unauthorized_user(self):
        self.assertEqual(Playlist.objects.count(), 0)
        data = {
            "name": "new playlist",
            "description": "custom description",
        }
        response = self.client_unauthenticated.post(reverse('playlist-list'), data=data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Playlist.objects.count(), 0)
