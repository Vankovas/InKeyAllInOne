from django.urls import reverse

from creator.models import Song
from user.models import Playlist, PlaylistTrack
from user.tests.test_playlist_viewset.playlist_mixin import TestPlaylistMixin


class TestPlaylistUpdateViewSet(TestPlaylistMixin):
    def test_delete_works(self):
        id_to_delete = self.playlists[2].id
        self.assertEqual(Playlist.objects.filter(pk=id_to_delete).count(), 1)
        response = self.client.delete(reverse('playlist-detail', kwargs={"pk": id_to_delete}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Playlist.objects.filter(pk=id_to_delete).count(), 0)

    def test_delete_works_and_removes_tracks(self):
        id_to_delete = self.playlists[0].id
        self.assertEqual(Playlist.objects.filter(pk=id_to_delete).count(), 1)
        self.assertEqual(PlaylistTrack.objects.count(), 2)
        self.assertEqual(Song.objects.count(), 3)

        response = self.client.delete(reverse('playlist-detail', kwargs={"pk": id_to_delete}))

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Playlist.objects.filter(pk=id_to_delete).count(), 0)
        self.assertEqual(PlaylistTrack.objects.count(), 0)
        # assert no songs have been deleted
        self.assertEqual(Song.objects.count(), 3)

    def test_delete_another_persons_playlist(self):
        id_to_delete = self.playlists[1].id
        self.assertEqual(Playlist.objects.filter(pk=id_to_delete).count(), 1)
        response = self.client.delete(reverse('playlist-detail', kwargs={"pk": id_to_delete}))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Playlist.objects.filter(pk=id_to_delete).count(), 1)

    def test_delete_unauthenticated_user_doesnt_work(self):
        id_to_delete = self.playlists[1].id
        self.assertEqual(Playlist.objects.filter(pk=id_to_delete).count(), 1)
        response = self.client_unauthenticated.delete(reverse('playlist-detail', kwargs={"pk": id_to_delete}))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Playlist.objects.filter(pk=id_to_delete).count(), 1)

