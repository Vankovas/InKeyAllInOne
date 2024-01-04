from django.urls import reverse
from user.tests.test_playlist_viewset.playlist_mixin import TestPlaylistMixin


class TestPlaylistUpdateViewSet(TestPlaylistMixin):
    def test_update_works_correctly(self):
        data = {
            "name": "Name NO U!",
            "description": "another description",
        }
        response = self.client.patch(reverse('playlist-detail', kwargs={"pk": self.playlists[0].id}), data=data)
        self.assertEqual(response.status_code, 200)
        self.playlists[0].refresh_from_db()
        self.assertEqual(self.playlists[0].name, "Name NO U!")
        self.assertEqual(self.playlists[0].description, "another description")

    def test_update_playlist_by_adding_songs(self):
        data = {
            "add_songs": [self.songs[2].id, self.songs[1].id],
        }
        self.assertEqual(self.playlists[2].songs.count(), 0)
        response = self.client.patch(reverse('playlist-detail', kwargs={"pk": self.playlists[2].id}), data=data)
        self.assertEqual(response.status_code, 200)
        self.playlists[2].refresh_from_db()
        self.assertEqual(self.playlists[2].songs.count(), 2)
        self.assertEqual(self.playlists[2].songs.filter(pk=self.songs[2].id).count(), 1)
        self.assertEqual(self.playlists[2].songs.filter(pk=self.songs[1].id).count(), 1)
        self.assertEqual(self.playlists[2].songs.filter(pk=self.songs[0].id).count(), 0)

    def test_update_playlist_by_deleting_songs(self):
        data = {
            "delete_songs": [self.songs[2].id],
        }
        self.assertEqual(self.playlists[0].songs.count(), 2)
        response = self.client.patch(reverse('playlist-detail', kwargs={"pk": self.playlists[0].id}), data=data)
        self.assertEqual(response.status_code, 200)
        self.playlists[0].refresh_from_db()
        self.assertEqual(self.playlists[0].songs.count(), 1)
        self.assertEqual(self.playlists[0].songs.first().id, self.songs[1].id)

    def test_deleting_a_song_which_doesnt_exist_in_playlist_doesnt_do_anything(self):
        data = {
            "delete_songs": [self.songs[2].id],
        }
        self.assertEqual(self.playlists[2].songs.count(), 0)
        response = self.client.patch(reverse('playlist-detail', kwargs={"pk": self.playlists[2].id}), data=data)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.playlists[2].refresh_from_db()
        self.assertEqual(self.playlists[2].songs.count(), 0)

    def test_adding_a_song_for_the_second_time_doent_add_it_again(self):
        data = {
            "add_songs": [self.songs[2].id, self.songs[2].id],
        }
        self.assertEqual(self.playlists[2].songs.count(), 0)
        response = self.client.patch(reverse('playlist-detail', kwargs={"pk": self.playlists[2].id}), data=data)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.playlists[2].refresh_from_db()
        self.assertEqual(self.playlists[2].songs.count(), 1)
        self.assertEqual(self.playlists[2].songs.all()[0].id, self.songs[2].id)

    def test_updating_another_users_playlist_fails(self):
        data = {
            "name": "Name NO U!",
        }
        response = self.client.patch(reverse('playlist-detail', kwargs={"pk": self.playlists[1].id}), data=data)
        self.assertEqual(response.status_code, 403)
        self.playlists[1].refresh_from_db()
        self.assertEqual(self.playlists[1].name, "Name 2")

    def test_unauthenticated_user_fails(self):
        data = {
            "name": "Name NO U!",
        }
        response = self.client_unauthenticated.patch(
            reverse('playlist-detail', kwargs={"pk": self.playlists[1].id}), data=data)
        self.assertEqual(response.status_code, 401)
        self.playlists[1].refresh_from_db()
        self.assertEqual(self.playlists[1].name, "Name 2")
