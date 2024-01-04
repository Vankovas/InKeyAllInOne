from cloudinary_storage.storage import MediaCloudinaryStorage
from django.core.exceptions import ValidationError
from django.db import models
from core.abstract_models import AbstractVote, AbstractViewsRatingAndCreatedTime


def cover_path(album, filename):
    email = album.artist.email.replace(".", "_")
    email = email.replace("@", "_")
    return f'user_{email}/{album.name}/cover/{filename}'


def validate_image_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.png', '.jpeg', '.gif', '.jpg', ".webp"]
    if ext not in valid_extensions:
        raise ValidationError(u'File not supported!')


def song_path(song, filename):
    email = song.album.artist.email.replace(".", "_")
    email = email.replace("@", "_")
    return f'user_{email}/{song.album.name}/{filename}'


def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.mp3', '.wav', '.mp4']
    if ext not in valid_extensions:
        raise ValidationError(u'File not supported!')


class Album(AbstractViewsRatingAndCreatedTime):
    artist = models.ForeignKey("account_management.User", on_delete=models.CASCADE, related_name="albums")
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, blank=True, default='')
    cover_image = models.ImageField(upload_to=cover_path, validators=[validate_image_extension], blank=True,
                                    storage=MediaCloudinaryStorage(), null=True, default=None)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Song(AbstractViewsRatingAndCreatedTime):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, blank=True, default='')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="songs")
    data = models.FileField(upload_to=song_path, validators=[validate_file_extension])

    def __str__(self):
        return self.name


class SongVote(AbstractVote):
    key_containing_rating = "song"
    user = models.ForeignKey("account_management.User", on_delete=models.CASCADE, related_name="song_votes")
    song = models.ForeignKey('creator.Song',  on_delete=models.CASCADE, related_name="votes")


class AlbumVote(AbstractVote):
    key_containing_rating = "album"
    user = models.ForeignKey("account_management.User", on_delete=models.CASCADE, related_name="album_votes")
    album = models.ForeignKey('creator.Album',  on_delete=models.CASCADE, related_name="votes")