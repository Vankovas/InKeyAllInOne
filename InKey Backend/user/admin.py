from django.contrib import admin
from .models import Playlist
from .models import PlaylistTrack
from .models import Comment
from .models import Stream
from .models import CommentAlbum, CommentSong
from .models import FavoriteAlbum
from .models import FavoriteSong
from .models import FavoriteArtist


admin.site.register(Playlist)
admin.site.register(PlaylistTrack)
admin.site.register(Comment)
admin.site.register(CommentAlbum)
admin.site.register(CommentSong)
admin.site.register(FavoriteAlbum)
admin.site.register(FavoriteSong)
admin.site.register(FavoriteArtist)
admin.site.register(Stream)
# Register your models here.
