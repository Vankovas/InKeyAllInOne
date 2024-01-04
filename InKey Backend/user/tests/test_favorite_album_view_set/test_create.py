from http import HTTPStatus
from django.urls import reverse
from account_management.tests.mixin.test_user_mixin import TestUserMixin
from creator.models import Album
from user.models import FavoriteAlbum


class TestCreateFavoriteAlbumViewSet(TestUserMixin):
    def setUp(self) -> None:
        super(TestCreateFavoriteAlbumViewSet, self).setUp()
        self.own_album = Album.objects.create(artist=self.user, name="own album")
        self.album = Album.objects.create(artist=self.user_other, name="new album")

    def test_add_to_favorite_works(self):
        data = {
            'album_id': self.album.id
        }
        response = self.client.post(reverse("favorite_album-list"), data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_add_to_favorite_twice_delete(self):
        data = {
            'album_id': self.album.id
        }
        self.client.post(reverse("favorite_album-list"), data)
        print(f'Album is added to database: {FavoriteAlbum.objects.all()}')
        response = self.client.post(reverse("favorite_album-list"), data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        print(f'Album is removed from database: {FavoriteAlbum.objects.all()}')

    def test_add_to_favorite_no_such_album(self):
        data = {
            'album_id': self.album.id+1
        }
        response = self.client.post(reverse("favorite_album-list"), data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_add_favorite_album_unauthenticated(self):
        data = {
            'album_id': self.album.id
        }
        response = self.client_unauthenticated.post(reverse("favorite_album-list"), data)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_you_cannot_like_your_own_album(self):
        data = {
            'album_id': self.own_album.id
        }
        response = self.client.post(reverse("favorite_album-list"), data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)