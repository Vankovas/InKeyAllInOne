import os
# -*- coding: utf-8 -*-
import os
import django

#  you have to set the correct path to you settings module
from django.db.models import Count

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from account_management.models import User
from creator.models import Album, Song

if __name__ == '__main__':
    for user in User.objects.all():
        duplicate_albums = Album.objects.filter(artist=user).\
            values('name').annotate(email_count=Count('name')).filter(email_count__gt=1)
        for data in duplicate_albums:
            name = data['name']
            objs = Album.objects.filter(artist=user, name=name).order_by('pk')[1:]
            for obj in objs:
                obj.delete()

    for album in Album.objects.all():
        duplicate_songs = Song.objects.filter(album=album).\
            values('name').annotate(email_count=Count('name')).filter(email_count__gt=1)
        for data in duplicate_songs:
            name = data['name']
            objs = Song.objects.filter(album=album, name=name).order_by('pk')[1:]
            for obj in objs:
                obj.delete()




