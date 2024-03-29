# Generated by Django 2.2.6 on 2020-06-04 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('creator', '0005_auto_20200511_1727'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentalbum',
            name='album',
        ),
        migrations.RemoveField(
            model_name='commentalbum',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='commentsong',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='commentsong',
            name='song',
        ),
        migrations.RemoveField(
            model_name='favoritealbum',
            name='album',
        ),
        migrations.RemoveField(
            model_name='favoritealbum',
            name='user',
        ),
        migrations.RemoveField(
            model_name='favoriteartist',
            name='artist',
        ),
        migrations.RemoveField(
            model_name='favoriteartist',
            name='user',
        ),
        migrations.RemoveField(
            model_name='favoritesong',
            name='song',
        ),
        migrations.RemoveField(
            model_name='favoritesong',
            name='user',
        ),
        migrations.RemoveField(
            model_name='playlist',
            name='artist',
        ),
        migrations.RemoveField(
            model_name='songsinplaylist',
            name='playlist',
        ),
        migrations.RemoveField(
            model_name='songsinplaylist',
            name='song',
        ),
        migrations.RemoveField(
            model_name='stream',
            name='artist',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='CommentAlbum',
        ),
        migrations.DeleteModel(
            name='CommentSong',
        ),
        migrations.DeleteModel(
            name='FavoriteAlbum',
        ),
        migrations.DeleteModel(
            name='FavoriteArtist',
        ),
        migrations.DeleteModel(
            name='FavoriteSong',
        ),
        migrations.DeleteModel(
            name='Playlist',
        ),
        migrations.DeleteModel(
            name='SongsInPlaylist',
        ),
        migrations.DeleteModel(
            name='Stream',
        ),
    ]
