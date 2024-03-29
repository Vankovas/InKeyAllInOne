# Generated by Django 2.2.6 on 2020-05-11 15:27

import creator.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('creator', '0004_comment_content_favoritecontent_playlist_rating_songsinplaylist_stream'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentAlbum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='CommentSong',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentsSong', to='creator.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteAlbum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteArtist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_favorites', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fav_artists', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteSong',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='favoritecontent',
            name='content',
        ),
        migrations.RemoveField(
            model_name='favoritecontent',
            name='user',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='user',
        ),
        migrations.RenameField(
            model_name='playlist',
            old_name='creator',
            new_name='artist',
        ),
        migrations.AddField(
            model_name='album',
            name='cover_image',
            field=models.ImageField(blank=True, upload_to=creator.models.cover_path, validators=[creator.models.validate_image_extension]),
        ),
        migrations.AddField(
            model_name='song',
            name='rating',
            field=models.FloatField(default=0, max_length=5),
        ),
        migrations.DeleteModel(
            name='Content',
        ),
        migrations.DeleteModel(
            name='FavoriteContent',
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
        migrations.AddField(
            model_name='favoritesong',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_favorites', to='creator.Song'),
        ),
        migrations.AddField(
            model_name='favoritesong',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fav_songs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='favoritealbum',
            name='album',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_favorites', to='creator.Album'),
        ),
        migrations.AddField(
            model_name='favoritealbum',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fav_albums', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='commentsong',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentsSong', to='creator.Song'),
        ),
        migrations.AddField(
            model_name='commentalbum',
            name='album',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentsAlbum', to='creator.Album'),
        ),
        migrations.AddField(
            model_name='commentalbum',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentsAlbum', to='creator.Comment'),
        ),
    ]
