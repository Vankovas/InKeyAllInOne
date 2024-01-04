from http import HTTPStatus
from django.urls import reverse
from account_management.tests.mixin.test_user_mixin import TestUserMixin
from creator.models import Album
from user.models import FavoriteAlbum


class TestListFavoriteAlbumViewSet(TestUserMixin):
    def setUp(self) -> None:
        super(TestListFavoriteAlbumViewSet, self).setUp()
        self.album = [
            Album.objects.create(artist=self.user_other, name="album 1"),
            Album.objects.create(artist=self.user, name="album 2"),
            Album.objects.create(artist=self.user_other, name="album 3")
        ]
        self.favorite_albums = [
            FavoriteAlbum.objects.create(user_id=self.user.id, album_id=self.album[0].id),
            FavoriteAlbum.objects.create(user_id=self.user.id, album_id=self.album[2].id)
        ]

    def test_list_favorite_albums_unauthenticated(self):
        response = self.client_unauthenticated.get(reverse("favorite_album-list"))
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_favorite_albums_works(self):
        response = self.client.get(reverse("favorite_album-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        all_albums = response.json()
        self.assertEqual(len(all_albums), 2)
