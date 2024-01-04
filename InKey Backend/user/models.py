import uuid as uuid
from django.db import models

from core.abstract_models import AbstractVote, AbstractViewsRatingAndCreatedTime
from creator.models import Album, Song


class Playlist(AbstractViewsRatingAndCreatedTime):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2000)
    user = models.ForeignKey("account_management.User", on_delete=models.CASCADE, related_name="playlists")
    songs = models.ManyToManyField('creator.Song', through='user.PlaylistTrack',
                                   through_fields=["playlist", "song"])

    def __str__(self):
        return self.name


class PlaylistVote(AbstractVote):
    key_containing_rating = "playlist"
    playlist = models.ForeignKey('user.Playlist',  on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey("account_management.User", on_delete=models.CASCADE, related_name="playlist_votes")


class PlaylistTrack(models.Model):
    playlist = models.ForeignKey('user.Playlist', on_delete=models.CASCADE, related_name="all_playlist_tracks")
    song = models.ForeignKey('creator.Song', on_delete=models.CASCADE, related_name="all_playlist_tracks")
    position = models.IntegerField(default=0)

    class Meta:
        ordering = ['position']

    @classmethod
    def last_position(cls, playlist):
        last_track = cls.objects.filter(playlist=playlist).order_by("-position").first()
        if last_track:
            return last_track.position
        return 0


class Comment(models.Model):
    user = models.ForeignKey("account_management.User", on_delete=models.CASCADE, related_name="comments")
    date_of_creation = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=1000)


class CommentAlbum(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="commentsAlbum")
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="commentsAlbum")


class CommentSong(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="commentsSong")
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="commentsSong")


class Stream(models.Model):
    artist = models.OneToOneField("account_management.User", on_delete=models.CASCADE, related_name="stream")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class FavoriteSong(models.Model):
    user = models.ForeignKey("account_management.User", on_delete=models.CASCADE, related_name="fav_songs")
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="in_favorites")


class FavoriteAlbum(models.Model):
    user = models.ForeignKey("account_management.User", on_delete=models.CASCADE, related_name="fav_albums")
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="in_favorites")


class FavoriteArtist(models.Model):
    user = models.ForeignKey("account_management.User", on_delete=models.CASCADE, related_name="fav_artists")
    artist = models.ForeignKey("account_management.User", on_delete=models.CASCADE, related_name="in_favorites")

