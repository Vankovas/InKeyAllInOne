from account_management.tests.mixin.test_user_mixin import TestUserMixin
from creator.models import Album, Song
from user.models import Playlist, PlaylistTrack


class TestPlaylistMixin(TestUserMixin):
    def setUp(self) -> None:
        super(TestPlaylistMixin, self).setUp()
        self.album = Album.objects.create(artist=self.user_other, name="new album")
        self.songs = [
            Song.objects.create(name="song1", album=self.album),
            Song.objects.create(name="song2", album=self.album),
            Song.objects.create(name="song3", album=self.album)
        ]
        self.playlists = [
            Playlist.objects.create(user=self.user, name="Name 1", description="haha"),
            Playlist.objects.create(user=self.user_other, name="Name 2", description="hihi"),
            Playlist.objects.create(user=self.user, name="Name 3", description="huhu"),
        ]
        self.tracks = [
            PlaylistTrack.objects.create(playlist=self.playlists[0], song=self.songs[2], position=0),
            PlaylistTrack.objects.create(playlist=self.playlists[0], song=self.songs[1], position=1),
        ]